import json
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from AdresseParser import AdresseParser
import re
import validators
import requests


warnings.filterwarnings("ignore", category=DeprecationWarning)





if __name__ == '__main__':

    df = pd.DataFrame(
        columns=[
            'code',
            'latitude',
            'longitude',
            'name',
            'address',
            'address2',
            'postalCode',
            'city',
            'department',
            'capacity',
            'capacityReducedMobility',
            'Link'
        ])
    with open("ObjectifCode/extracts/ObjectifCode012023.json", "r") as f:
        data = json.load(f)
    # on rentre les identifiants de connexion
    for i in tqdm(range(len(data))):
        row = [            
            data[i]['code'],
            data[i]['latitude'],
            data[i]['longitude'],
            data[i]['name'],
            data[i]['address'],
            data[i]['address2'],
            data[i]['postalCode'],
            data[i]['city'],
            data[i]['department'],
            data[i]['capacity'],
            data[i]['capacityReducedMobility'],
            f"https://www.objectifcode.sgs.com{data[i]['linkCenter']}"
        ]
        df.loc[len(df)] = row
df.to_csv('ObjectifCode/extracts/ObjectifCode012023.csv', header=True, index=False)