import js2py
import csv
import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')

obj = {}
PATH = '20230522.js'
with open(PATH, 'r') as f:
    js_data = f.read()



# Convert JavaScript to Python
context = js2py.EvalJs()
context.execute(js_data)

# Extract locations
locations = context.locations.to_list()

# Write the dictionaries to a CSV file
with open(f'extracts/extract_ObjectifCode_{current_date}.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=locations[0].keys())
    writer.writeheader()
    writer.writerows(locations)