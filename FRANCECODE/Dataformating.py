import json
from tqdm import tqdm
import pandas as pd
with open("FRANCECODE/extracts/extrat_raw_0123.json", "r") as f:
        decoded_data=f.readline().encode().decode('utf-8-sig') 
        data = json.loads(decoded_data)


data_df = pd.json_normalize(data)
data_df['links'] =list(map(lambda x:x['callsToAction'][0]['pivot_button_value'], data))
data_df = data_df[['id', 'name', 'lat', 'lng', 'phone', 'email', 'slug', 'visible', 'address', 'display_address', 'address_line_1', 'city', 'state', 'postcode', 'links']]
data_df.to_csv('FRANCECODE/extracts/extrat_FRANCECODE_012023.csv',encoding='utf-8-sig', sep=";", index=False, header=True)