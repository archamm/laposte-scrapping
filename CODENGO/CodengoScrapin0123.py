import json
import pandas as pd
from bs4 import BeautifulSoup


f = open('CODENGO/extract/extractRaw_Codengo_0123.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list


df = pd.DataFrame(
        columns=['id', 'name',  'address', 'zipCode', 'city', "info", 'status', 'latitude', 'longitude'])



for dept in data['data']:
    for site in dept['siteLiteDtoList']:
        row = [site['id'], site['name'], site['address'], site['zipCode'], site['city'], BeautifulSoup(site['landmark'], "lxml").text, site['status'], site['latitude'], site['longitude']]
        df.loc[len(df)] = row

df.to_csv('CODENGO/extract/extrat_CODENGO_012023_v2.csv', encoding='utf-8-sig', header=True, index=False)

# Closing file
f.close()