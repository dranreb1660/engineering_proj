import numpy as np
import pandas as pd
import os
import torch
import pickle
import psycopg2
from IPython import display
from fpl_engineering.data.base_dataset import make_sequences
from fpl_engineering.utils import get_project_root, transform_sequences, target_descaler

project_root = str(get_project_root())
artifact_dir = 'artifacts/trained-model:v5'


user = 'postgres'
password = os.environ.get('DB_PASS')
database = 'fantasypl'
conn_string = f'postgresql://{user}:{password}@localhost:5432/{database}'

conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()

player = 357
round_ = 15
s_len = 5

sql1 = f'''
Select * from 
	(SELECT * FROM cleaned_history 
	 where element = {player} and round <= {round_}
	 ORDER BY round DESC limit {s_len}) 
as r ORDER BY round ASC;
'''
# cursor.execute(sql1)

with open(project_root+'/models/scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)

d = pd.read_sql(sql1,con=conn)
sequences = make_sequences(d, s_len, labels=False)

features = transform_sequences(sequences, scaler, s_len,35)
features = torch.tensor(features, dtype=torch.float)

model = torch.load(artifact_dir+"/lstm_model.pth")

def predict(model, x):
  model.freeze()
  model.eval()
  y = model(x)

  pred = target_descaler(y.item())
  return pred

if __name__ == "__main__":
    display.display(d)
    print(features.shape)
    print(predict(model, features))
