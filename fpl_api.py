import pickle as pkl
import numpy as np
import pandas as pd
import sqlalchemy as sql

# lr_model is our simple logistic regression model
# lr_model.feature_names are the four different iris measurements
with open("./models/lr.pkl", "rb") as f:
    lr_model = pkl.load(f)

engine = sql.create_engine("sqlite:///fantasy.db")

feature_names = ['was_home(1 for home, 0 for away)', 'team_h_score', 'team_a_score',
                 'minutes', 'goals_scored', 'assists', 'clean_sheets', 'total_points']


def manual_prediction(feature_dict):
    """
    """
    x_input = [
        float(feature_dict.get(name, 0)) for name in feature_names
    ]

    predicted = round(lr_model.predict([x_input])[0])

    return x_input, predicted


def get_inputs():
    engine = sql.create_engine("sqlite:///fantasy.db")
    full_name_q = """
    SELECT  first_name || " " ||web_name
    FROM elements
    """

    all_full_names = np.sort(pd.read_sql(full_name_q, engine).values.flatten())

    all_round = list(range(1, 39))
    return all_full_names, all_round


def auto_prediction(full_name, round_):
    if not full_name or not round_:
        return 0
    full_name = str(full_name)
    round_ = int(round_)
    querry = f'''
    SELECT a.was_home, a.team_h_score,a.team_a_score, a.minutes, a.goals_scored, a.assists, a.clean_sheets, a.total_points
    FROM  elements as e
    JOIN all_weeks as a
    ON e.id=a.element
    WHERE e.first_name || " " || e.web_name = "{full_name}" and a.round = {round_}
    ORDER by a.round
    '''
    var = pd.read_sql(querry, engine).values
    answer = round(lr_model.predict(var)[0])

    return answer


    # This section checks that the prediction code runs properly
    # To run, type "python predictor_api.py" in the terminal.
    #
    # The if __name__='__main__' section ensures this code only runs
    # when running this file; it doesn't run when importing
if __name__ == '__main__':
    from pprint import pprint
    print("Checking to see what setting all params to 0 predicts")
    features = {f: '0' for f in feature_names}
    print('Features are')
    pprint(features)

    x_input, predicted = manual_prediction(features)
    print(f'Input values: {x_input}')
    print('Output probabilities')
    pprint(predicted)
