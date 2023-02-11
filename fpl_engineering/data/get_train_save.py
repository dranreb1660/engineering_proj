import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

import pickle as pkl
from sqlalchemy import create_engine

import sqlalchemy as sql
import sqlite3
import requests


def get_put_db():
    """
    This Function gets data from the Fantasy Api, extracts different sections and put them into differeent tables in a relational (sql) database. 
    """
    db_name = 'fantasy.db'
    conn = sqlite3.connect(db_name)

    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = requests.get(url)
    json = r.json()

    elem_df = pd.DataFrame(json['elements'])
    teams_df = pd.DataFrame(json['teams'])

    for i in elem_df.index:
        elem_id = elem_df.id[i]
        url = f'https://fantasy.premierleague.com/api/element-summary/{elem_id}/'
        r = requests.get(url)
        json = r.json()

        hostory_df = pd.DataFrame(json['history'])
        past_history = pd.DataFrame(json['history_past'])

        if i == 0:
            all_his = hostory_df.copy()
            all_past = past_history.copy()
        else:
            all_his = all_his.append(all_his)
            all_past = all_past.append(all_past)

    all_his['total_points_y'] = all_his.groupby(
        'element')['total_points'].shift(-1)
    all_his = all_his.groupby(
        'element', as_index=False, group_keys=False).apply(lambda x: x.iloc[:-1])
    all_his.reset_index().drop('index', axis=1)

    elem_df.to_sql('elements', con=conn)
    teams_df.to_sql('teams', con=conn)
    all_his.to_sql('all_weeks', con=conn)
    all_past.to_sql('prev_years', con=conn)


def make_model():
    """
    Theis fuction gets data from our sql database, uses the data to make a linear Regression model, then saves the model in our models folder
    """
    engine = sql.create_engine("sqlite:///fantasy.db")
    querry = """
    select element, was_home,team_h_score, team_a_score, minutes,goals_scored, assists, clean_sheets,total_points,  total_points_y from all_weeks
    
    """
    df = pd.read_sql(querry, engine)

    X = df.drop(['total_points_y', 'element'], axis=1)
    y = df['total_points_y']

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=200)

    # fit our model and score it on the test set
    lr_model = LinearRegression()
    lr_model.fit(x_train, y_train)

    print(f"""
    train score: {lr_model.score(x_train, y_train):%}
    test score: {lr_model.score(x_test, y_test):%}
    """)
    preds = lr_model.predict(x_test)

    # report results

#     print('Model Error')
#     print('MSE: ', mean_squared_error(y_test, preds))
#     print('MAE: ', mean_absolute_error(y_test, preds), '\n')

#     print('Feature coefficient results: \n')
#     for feature, coef in zip(X.columns, lr_model.coef_):
#         print(feature, ':', f'{coef:.2f}')

    with open("models/lr.pkl", "wb") as f:
        pkl.dump(lr_model, f)


get_put_db()
make_model()


