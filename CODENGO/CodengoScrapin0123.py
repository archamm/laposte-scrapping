import json
import pandas as pd
from bs4 import BeautifulSoup
import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')

import requests
output_file = f"CODENGO/response_{current_date}.json"

url = "https://codengo.bureauveritas.fr/public/session/liste.json"

response = requests.get(url)

data = response.json()
with open(output_file, 'w') as file:
        json.dump(data, file)

with open(output_file, 'r') as file:
        data = json.load(file)


df = pd.DataFrame(
        columns=['id', 'name',  'address', 'zipCode', 'city', "info", 'status', 'latitude', 'longitude'])



for site in data['data']['sites']:
    landmark = site['landmark']
    if landmark is not None:
        landmark_text = BeautifulSoup(landmark, "lxml").text
    else:
        landmark_text = ""
    row = [
        site['id'],
        site['name'],
        site['address'],
        site['zipCode'],
        site['city'],
        landmark_text,
        site['status'],
        site['latitude'],
        site['longitude']
    ]
    df.loc[len(df)] = row

print(len(df))
df.to_csv(f'CODENGO/extract/extrat_CODENGO_{current_date}.csv', encoding='utf-8-sig', header=True, index=False)

