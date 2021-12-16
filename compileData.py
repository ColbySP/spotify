import os
import pandas as pd

PATH = 'ENTER YOUR PATH HERE'
json_files = [pos_json for pos_json in os.listdir(PATH) if pos_json.endswith('.json')]

df = pd.DataFrame()
for file in json_files:
    data = pd.read_json(PATH + '/' + file).set_index('endTime')
    df = df.append(data)

df = df.sort_index()
df.to_csv('compiled_data.csv')
