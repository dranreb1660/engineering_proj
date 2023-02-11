import numpy as np
import pandas as pd
import os
import torch
import pickle
import psycopg2
from fpl_engineering.data.base_dataset import make_sequences
from fpl_engineering.utils import get_project_root, transform_sequences, target_descaler

# from dotenv import load_dotenv
# load_dotenv('.env')

seq_len = 5
n_features = 35

project_root = str(get_project_root())
artifact_dir = 'artifacts/trained-model:v5'

with open(project_root+'/models/scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)
model = torch.load(artifact_dir+"/lstm_model.pth")

user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
database = os.environ.get('POSTGRES_DB')
pg_port = os.environ.get('POSTGRES_PORT')

conn_string = f'postgresql://{user}:{password}@database:{pg_port}/{database}'

conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

def get_inputs():
    names_query = """
    SELECT  concat(first_name,' ', second_name)
    FROM elements
    ORDER BY second_name
    """
    rounds_query = """
        select distinct(round) from all_weeks
        where round >= 4
        order by round
    """
    names = pd.read_sql(names_query, con=conn).values.flatten()
    rounds = pd.read_sql(rounds_query, con=conn).values.flatten()+1

    return names, rounds

def predict(name, round_):
    if not name or not round_:
        return 0
    name = str(name)
    round_ = int(round_)
    query = f'''
    Select * from 
        (SELECT a.*
        FROM  elements as e
        JOIN cleaned_history as a
        ON e.id=a.element 
        WHERE concat(first_name, ' ', second_name) = '{name}' and a.round <= {round_}
        ORDER BY a.round DESC limit 5) 
    as r ORDER BY round ASC;
    '''
    data = pd.read_sql(query,con=conn)
    print('len is   == . ',len(data))
    sequences = make_sequences(data, seq_len, labels=False)

    features = transform_sequences(sequences, scaler, seq_len, n_features)
    features = torch.tensor(features, dtype=torch.float)

    model.freeze()
    model.eval()
    y = model(features)

    pred = target_descaler(y.item())
    return pred

if __name__ == '__main__':
    name = 'Brenden Aaronson'
    round_ = 11
    pred, _ = predict(name, round_)
    print(f'predicted points for {name} for gameweek {round_+1} is {pred}')

