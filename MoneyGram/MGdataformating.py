import json
from tqdm import tqdm
import pandas as pd
with open("MoneyGram\extract_raw_MG_0123.json", "r") as f:
        decoded_data=f.readline().encode().decode('utf-8-sig') 
        data = json.loads(decoded_data)

data_df = pd.json_normalize(data['locations'])

data_df.to_csv('MoneyGram/extracts/extrat_raw.csv',encoding='utf-8-sig', index=False, header=True)