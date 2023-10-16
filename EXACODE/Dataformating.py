import json
from tqdm import tqdm
import pandas as pd
with open("EXACODE/extracts/extrat_raw_0123.json", "r") as f:
        decoded_data=f.readline().encode().decode('utf-8-sig') 
        data = json.loads(decoded_data)

df = pd.DataFrame(
        columns=['id', 'nom',  'adresse', 'code_postal', 'ville', 'derniere_modification', 'email', 'site_web', 'numero'])

data_df = pd.json_normalize(data).drop(['agrementNumber', 'closedDays', 
    'onDemand', 'ignoreDelaiInscr', 'cr.id', 'cr.name',	'cr.region.id', 'defaultExaminateur.id',
    'defaultExaminateur.cr.id',	'defaultExaminateur.cr.name', 'defaultExaminateur.cr.region.id', 'defaultExaminateur.cr.region.name'], axis=1)

print(len(data_df))
print(data_df.head())
data_df = data_df.drop_duplicates()
print(len(data_df))
print(data_df.head())

data_df.to_csv('EXACODE/extracts/extracts_EXCODE_0123.csv',encoding='utf-8-sig', index=False, header=True)