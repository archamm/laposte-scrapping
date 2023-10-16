import json
from tqdm import tqdm
import pandas as pd
from datetime import datetime
import re

def get_columns_to_drop(columns):
        regex = re.compile(r'links*')
        regex2 = re.compile(r'profil*')
        columns = [i for i in columns if regex.match(i) or regex2.match(i)]
        for column in ['address.level4', 'address.level3', 'address.level1', 'geoPosition.type',
                'geo.@type', 'geoPosition.float', 'geoPosition.coordinates', 'category']:
                columns.append(column)
        print(columns)
        return columns

def parse_opening_hours(res):
        data = {}
        print(data)
        data['Mo'] = ''
        data['Tu'] = ''
        data['We'] = ''
        data['Th'] = ''
        data['Fr'] = ''
        data['Sa'] = ''
        data['Sa'] = ''
        for i in res['openingHours']:
                if len(i) == 0:
                        continue
                else :
                        data[i['dayOfWeek']] = ' '.join(list(map(lambda x: x['opens'] + ' - ' + x['closes'], i['hours'])))
        return data
        
with open("TiersLieux/extracts/extract_raw_TiersLieux.json", "r") as f:
        decoded_data=f.readline().encode().decode('utf-8-sig') 
        data = json.loads(decoded_data)


raw_json = []
for key in data['results']:
        if 'openingHours' in data['results'][key]:
                data['results'][key]['openingHours'] = parse_opening_hours(data['results'][key])

        try:
                data['results'][key]['created'] = datetime.fromtimestamp(data['results'][key]['created'])
                data['results'][key]['updated'] = datetime.fromtimestamp(data['results'][key]['updated'])
                del data['results'][key]["links"]

        except Exception:
                df = {}
        raw_json.append(data['results'][key])

data_df = pd.json_normalize(raw_json)
print(len(data_df))
data_df = data_df.drop(get_columns_to_drop(data_df.columns), axis=1)
data_df.to_csv('TiersLieux/extracts/extract_TiersLieux_0223.csv',encoding='utf-8-sig', index=False, header=True, sep=';')