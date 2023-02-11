import os, sys
import requests
from tqdm import tqdm
import pandas as pd
import psycopg2
import argparse
from sqlalchemy import create_engine

user = 'docker'
password = 'docker'     #os.environ.get('DB_PASS')
database = 'fantasydb'

conn_string = f'postgresql://{user}:{password}@localhost:5431/{database}'



# conn = psycopg2.connect(
#     host = "localhost",
#     port = '5432',
#     user = user,
#     password = password,
#     database = database,
# )

from fpl_engineering.utils import get_project_root

class FPL():
    """
    Class to download or load latest download statistics for every player in the Premier League. 
    url to download data from: https://fantasy.premierleague.com/api/bootstrap-static/"

    args:
        data_dir: directory to download or load data to or from. default is 'data'
        download_data: a boolean to download a fresh data or avoid download, which loads data from the 'data_dir' location above
        sql
        
    """
    def __init__(self, data_dir:str = 'data', download:bool = True, sql=True) -> None:

        db = create_engine(conn_string)
        self.conn = db.connect()

        self.sql = sql
        self.download = download
        self.data_dir = data_dir

        self.root = get_project_root()
        raw_path = os.path.join(self.data_dir, 'raw')
        raw_data_dir = os.path.join(self.root, raw_path)



        if self.download:
            print('Downloading latest Data from https://fantasy.premierleague.com. Hang tight!\n')
            all_his_list = []
            all_past_list = []
            url = "https://fantasy.premierleague.com/api/bootstrap-static/"
            response = requests.get(url)
            json = response.json()
            elem_df = pd.DataFrame(json['elements'])
            teams_df = pd.DataFrame(json['teams'])

            print(f'Fatching all statistics for all {len(elem_df)} players for current season\n')
            for row in tqdm(elem_df.itertuples(), total=len(elem_df), colour='green'):
                elem_id = row.id
                url = f'https://fantasy.premierleague.com/api/element-summary/{elem_id}/'
                r = requests.get(url)
                json = r.json()

                history_df = pd.DataFrame(json['history'])
                past_history = pd.DataFrame(json['history_past'])

                all_his_list.append(history_df)
                all_past_list.append(past_history)

            all_history_df = pd.concat(all_his_list)
            self.all_past_history_df = pd.concat(all_past_list)

            self.all_history_df = all_history_df.groupby('element', as_index=False, group_keys=False).apply(lambda x: x.iloc[:-1])
            self.all_history_df.reset_index().drop('index', axis=1)
            
            self.all_history_df.to_csv(str(raw_data_dir)+'/raw_history.csv', index=False)
            self.all_past_history_df.to_csv(str(raw_data_dir)+'/raw_past_history.csv', index=False)

            if self.sql:
                elem_df.to_sql('elements', con=self.conn, if_exists='replace',index=False)
                teams_df.to_sql('teams', con=self.conn, if_exists='replace',index=False)
                self.all_history_df.to_sql('all_weeks', con=self.conn, if_exists='replace',index=False)
                self.all_past_history_df.to_sql('prev_years', con=self.conn, if_exists='replace',index=False)        

        else:
            all_history_df = pd.read_csv(str(raw_data_dir)+'/raw_history.csv', )
            all_past_history_df = pd.read_csv(str(raw_data_dir)+'/raw_past_history.csv')

            self.all_history_df = all_history_df.groupby('element', as_index=False, group_keys=False).apply(lambda x: x.iloc[:-1])
            self.all_history_df.reset_index().drop('index', axis=1)

    
    def get_cleaned_df(self):
        processed_path = os.path.join(self.data_dir, 'processed')
        processed_data_dir = os.path.join(self.root, processed_path)

        self.cleaned_history = self.all_history_df.dropna(how = 'any')
        self.cleaned_history = self.cleaned_history.drop(['kickoff_time'], axis=1)
        self.cleaned_history[["influence", "creativity", "threat", "ict_index"]] = self.cleaned_history[["influence", "creativity", "threat", "ict_index"]].apply(pd.to_numeric)
        self.cleaned_history["was_home"] = self.cleaned_history["was_home"].astype(int)
       
        self.cleaned_history.to_csv(str(processed_data_dir)+'/cleaned_history.csv', index=False) 

        if self.sql:
            self.cleaned_history.to_sql('cleaned_history', con=self.conn, if_exists='replace', index=False)
            print('registered into db')
        return self.cleaned_history

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', default=False, help='download fresh data to database')
    parser.add_argument('-ns', '--no_sql', action='store_false', default=True, help='turn off saving data to sql database')
    args = parser.parse_args()
    config = vars(args)

    data = FPL(download=config['download'], sql=config['no_sql'],  data_dir='data')
    # print(data.get_cleaned_df())

    conn = psycopg2.connect(conn_string)
    conn.autocommit = True
    cursor = conn.cursor()


    
    sql1 = '''select * from cleaned_history where element= 30 ;'''
    # cursor.execute(sql1)
    # for i in cursor.fetchall():
    #     print(i)

    df =pd.read_sql(sql=sql1, con=conn)
    print(df)
        



        