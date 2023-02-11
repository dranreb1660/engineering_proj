import pandas as pd
import requests


def get_put_db():
    """
    This Function gets data from the Fantasy Api, extracts different sections and put them into differeent tables in a relational (sql) database. 
    """

    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = requests.get(url)
    json = r.json()

    elem_df = pd.DataFrame(json['elements'])
    teams_df = pd.DataFrame(json['teams'])

    for i,row in elem_df.iterrows():
        elem_id = row['id']
        url = f'https://fantasy.premierleague.com/api/element-summary/{elem_id}/'
        r = requests.get(url)
        json = r.json()

        history_df = pd.DataFrame(json['history'])
        past_history = pd.DataFrame(json['history_past'])

        if i == 0:
            all_his = history_df.copy()
            all_past = past_history.copy()
        else:
            all_his = pd.concat([all_his,all_his])
            all_past = pd.concat([all_past,all_past])
        print(i)
    print('done with loop')

    all_his['total_points_y'] = all_his.groupby(
        'element')['total_points'].shift(-1)
    all_his = all_his.groupby(
        'element', as_index=False, group_keys=False).apply(lambda x: x.iloc[:-1])
    all_his.reset_index().drop('index', axis=1)

    elem_df.to_csv('elements', index=False)
    teams_df.to_csv('teams', index=False)
    all_his.to_csv('all_weeks', index=False)
    all_past.to_csv('prev_years', index=False)


get_put_db()

