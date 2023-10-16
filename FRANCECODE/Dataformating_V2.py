import json
import pandas as pd
from collections import OrderedDict



data_df = pd.read_csv('FRANCECODE/extracts/extrat_raw_012023.csv', sep=';')
print(data_df.columns)

data_df['links'] =list(map(lambda x:x['buttons'][0]['pivot_button_value'], data))
print(data_df.columns)
data_df.to_csv('FRANCECODE/extracts/extract_FRANCECODE_012023.csv',encoding='utf-8-sig', index=False, header=True)

