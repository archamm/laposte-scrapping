import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from deepparse import parser
import requests
from requests.structures import CaseInsensitiveDict

import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')


REQUEST_URL = 'https://exacode.fr/api/sessions/findces?latitude=50.6138111&longitude=3.0423599&earliest=2022-08-31'


def scrap_results(results, res):
    print(results.json())
    res += results.json()


if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['name',  'adress', 'postal_code', 'town'])
    data = pd.read_csv('EXACODE/villes_france.csv', header=None, usecols=[19,20])
    print(data.columns)
    for col in data.columns:
        print(col)
    res = []
    # on rentre les identifiants de connexion
    for i in tqdm(range(len(data))):
        headers = CaseInsensitiveDict()
        headers["Accept"] = "application/json"
        print(f'latitude={data.iloc[i, 1]}&longitude={data.iloc[i, 0]}')
        page = requests.get(f'https://exacode.fr/api/sessions/findces?latitude={data.iloc[i, 1]}&longitude={data.iloc[i, 0]}&earliest=2022-08-31', headers=headers)
        scrap_results(page, res)


    #df.to_csv('DEKRA/extracts/extrat_DEKRA.csv', encoding='utf-8-sig', header=True)
    with open('EXACODE/extracts/extrat_raw_0123.csv', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))

    df = pd.DataFrame(
        columns=['id', 'nom',  'adresse', 'code_postal', 'ville', 'derniere_modification', 'email', 'site_web', 'numero'])

    data_df = pd.json_normalize(res).drop(['agrementNumber', 'closedDays', 
        'onDemand', 'ignoreDelaiInscr', 'cr.id', 'cr.name',	'cr.region.id', 'defaultExaminateur.id',
        'defaultExaminateur.cr.id',	'defaultExaminateur.cr.name', 'defaultExaminateur.cr.region.id', 'defaultExaminateur.cr.region.name'], axis=1)

    print(len(data_df))
    print(data_df.head())
    data_df = data_df.drop_duplicates()
    print(len(data_df))
    print(data_df.head())

    data_df.to_csv(f'EXACODE/extracts/extracts_EXCODE_{current_date}.csv',encoding='utf-8-sig', header=True)
