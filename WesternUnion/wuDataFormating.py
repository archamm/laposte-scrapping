import pandas as pd
import json

# Read JSON file
json_file_path = 'WesternUnion/extracts/extrat_WesternUnion_0723.json'

with open(json_file_path, 'r') as file:
    data = json.load(file)


# Create an empty list to store the extracted data

extracted_data = []

for result in data:
    try: 
        for location in result['data']['locations']['results']:
            extracted_data.append(location)
    except Exception:
        print(result)



# Convert to DataFrame
df = pd.json_normalize(extracted_data)
print(len(df))

# Convert DataFrame to CSV
csv_file_path = 'WesternUnion/extracts/extract_WesternUnion_0723.csv.csv'
df.to_csv(csv_file_path, index=False)
df = pd.read_csv(csv_file_path)
df.drop_duplicates(subset=['orig_id'], inplace=True)
print(len(df))

df = df[df['country'] == 'FR']

print(len(df))

columns_ordered = [
    "locator_id", "orig_id", "name", "searchName", "location", "latitude", "longitude",
    "city", "state", "postal", "country", "2CharCountryISO", "COUNTRY_NAME", "formattedAddress",
    "streetAddress", "streetAddress2", "streetAddress3", "atmLocation", 
    "monOpenTime", "monCloseTime", "tueOpenTime", "tueCloseTime", 
    "wedOpenTime", "wedCloseTime", "thuOpenTime", "thuCloseTime", 
    "friOpenTime", "friCloseTime", "satOpenTime", "satCloseTime", 
    "sunOpenTime", "sunCloseTime", "time_zone", "tzOffset",
    "desktopHours.desktopHours.Monday", "desktopHours.desktopHours.Tuesday", 
    "desktopHours.desktopHours.Wednesday", "desktopHours.desktopHours.Thursday",
    "desktopHours.desktopHours.Friday", "desktopHours.desktopHours.Saturday", 
    "desktopHours.desktopHours.Sunday",
    "detail.hours.Monday", "detail.hours.Tuesday", "detail.hours.Wednesday", 
    "detail.hours.Thursday", "detail.hours.Friday", "detail.hours.Saturday", 
    "detail.hours.Sunday",
    "phone", "s_phone", "agentPaymentType", "bankAccountRequired", "type", 
    "distance", "networkName", "is_dormant", "NAID", "id", "CODECL", 
    "stage_and_pay", "Spanish_Message", "English_Message", "services", 
    "detailsUrl", "sendToCuba", "actionFilter", "detail.services", 
    "agentCurrency.agentCurrency", "desktopServices.desktopServices"
]

df = df[columns_ordered]

df.to_csv('WesternUnion/extracts/extract_WesternUnion_0723_clean.csv', index=False)

print("CSV file created successfully.")