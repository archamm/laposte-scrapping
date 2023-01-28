import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from deepparse import parser
import requests
from requests.structures import CaseInsensitiveDict




REQUEST_URL = 'https://exacode.fr/api/sessions/findces?latitude=50.6138111&longitude=3.0423599&earliest=2022-08-31'
PATH = 'DEKRA/response.html'


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


