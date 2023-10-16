import json
import pandas as pd
from tqdm import tqdm
import requests
from requests.structures import CaseInsensitiveDict

import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')



if __name__ == '__main__':

    res = []
    # on rentre les identifiants de connexion
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    page = requests.get(f'https://storerocket.io/api/user/Yw8l7XrJvo/locations?limit=100', headers=headers)
    res += page.json()['results']['locations']
    print(len(res))
    data_df = pd.json_normalize(res)
    data_df['links'] =list(map(lambda x:x['callsToAction'][0]['pivot_button_value'], res))
    data_df = data_df[['id', 'name', 'lat', 'lng', 'phone', 'email', 'slug', 'visible', 'address', 'display_address', 'address_line_1', 'city', 'state', 'postcode', 'links']]
    data_df.to_csv(f'FRANCECODE/extracts/extrat_FRANCECODE_{current_date}.csv',encoding='utf-8-sig', sep=";", index=False, header=True)


