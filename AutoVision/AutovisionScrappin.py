import js2py
import csv
import datetime
import pandas as pd


current_date = datetime.datetime.now().strftime('%Y%m%d')

obj = {}
PATH = 'AutoVision/20230525.js'
with open(PATH, 'r') as f:
    js_data = f.read()



# Convert JavaScript to Python
context = js2py.EvalJs()
context.execute(js_data)

# Extract locations
locations = context.CentresList.to_list()

# Write the dictionaries to a CSV file
data_df = pd.json_normalize(locations)
data_df.to_csv(f'AutoVision/extracts/extract_AutoVision_{current_date}.csv',encoding='utf-8-sig', header=True)
