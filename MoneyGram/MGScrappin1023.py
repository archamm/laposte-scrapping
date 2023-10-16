
import json
import pandas as pd
import requests
import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')

cookies = {
    'IR_16828': '1696354113105%7C0%7C1696354113105%7C%7C',
    'IR_gbd': 'moneygram.com',
    '_ga': 'GA1.2.687564181.1696354113',
    '_ga_419TZ53GJ4': 'GS1.1.1696354113.1.0.1696354113.0.0.0',
    '_gat_UA-42673143-1': '1',
    '_gid': 'GA1.2.423624865.1696354113',
    'cmapi_cookie_privacy': 'permit 1,2,3,4',
    'cmapi_gtm_bl': '',
    'notice_gdpr_prefs': '0,1,2,3:',
    'notice_preferences': '3:',
    'nlbi_2222183_2147483392': 'EM8TWdHJOU5isY6xUnWprgAAAAAEjIlYt+6ISG3sx4Vljawk',
    'reese84': '3:XldzlhwUpaDKUjKI5gUa4Q==:BmsrkbScKpWMy90DU0BWDLsWkXhTRQ8yItBIWVQViQpZOmOD+V1wqZCoNE0puztkrEKpWF6OmvDJoRkOmZsjCvqL/9lo3zpoqUqEUFIzhsJ1r5xR/yVwj8iRhff44+66wTBY3DAiISYMt/wwaDXb5aDuJutLYJ6uwJfGJWl1qOJW4iiq4NGLSRUKXwdb/QMEPEUjDq9kv5g1A/aQs8LDVcS+bQQASbdojE7IDbfoKdIANyxKx6BEe6NNzELG1jZ/+w7R46/tkg4dGqW0b03Sjqqj4jybW8PlvQq8IgWColMOl7XW405W9nedeuOrP5iUEKb3MGHfrWpaMJRsLOZpJmTgsuwrRAk1v2W7nJz3tzjS1nyrBGKuydDX21Q5h17r99FxH1R5Mv9/AfFRw3RzolHwyVRg3sQG1gaqGUjUKXn65mIKKAUgxRscVdX+P+x6MyGm4+7EkXmxGRRzkC05hL4heyBG9RLBbPI7Ev6dAtIkhdZaOuOEwqr0mfVyjCLW:orSvciapnuJo0Ca7E9LRtLvJRWlZMRttQAhwDVBCqgA=',
    'TAsessionID': '363f7709-3a31-4198-951a-94be3c009b11|NEW',
    '_gcl_au': '1.1.106579617.1696354064',
    '_gcl_aw': 'GCL.1696354064.EAIaIQobChMIu4u8qLPagQMVTz4GAB3bqw14EAAYASAAEgKIP_D_BwE',
    '_gcl_dc': 'GCL.1696354064.EAIaIQobChMIu4u8qLPagQMVTz4GAB3bqw14EAAYASAAEgKIP_D_BwE',
    '_rdt_uuid': '1696354064693.0dcd6c3a-655b-483e-88d3-03c57640a6e0',
    'incap_ses_390_2163526': '4cX9ML1v6X5h42D0epBpBRBPHGUAAAAA79f8Ip/4mj5HXK3PsSdKuA==',
    'nlbi_2163526': 'qOC0Ig+1yhoEAPDoB1D/egAAAACUGLYcEr22rEAscDAxyBxT',
    'notice_behavior': 'implied,eu',
    'visid_incap_2163526': 'R0D6IWbxQPiwSRS7Y/jZGRBPHGUAAAAAQUIPAAAAAAClVVnHaiedXY+y1vZqJqYq',
    'incap_ses_390_2222183': 'v9fAc/hETS7p32D0epBpBQ5PHGUAAAAAoH8C+fdQS1xNcdOl1UXF0A==',
    'nlbi_2222183': '5gtyAQhMnFDRmxTDUnWprgAAAADZxm4h+HzWyF3AzWBG+iK5',
    'visid_incap_2222183': 'auOYClrQRtaPTndI66QXvA5PHGUAAAAAQUIPAAAAAABO3B94R5Rixh+GHo4s8ffd',
}

headers = {
    'Accept': 'application/json',
    'Origin': 'https://www.moneygram.com',
    # 'Cookie': 'IR_16828=1696354113105%7C0%7C1696354113105%7C%7C; IR_gbd=moneygram.com; _ga=GA1.2.687564181.1696354113; _ga_419TZ53GJ4=GS1.1.1696354113.1.0.1696354113.0.0.0; _gat_UA-42673143-1=1; _gid=GA1.2.423624865.1696354113; cmapi_cookie_privacy=permit 1,2,3,4; cmapi_gtm_bl=; notice_gdpr_prefs=0,1,2,3:; notice_preferences=3:; nlbi_2222183_2147483392=EM8TWdHJOU5isY6xUnWprgAAAAAEjIlYt+6ISG3sx4Vljawk; reese84=3:XldzlhwUpaDKUjKI5gUa4Q==:BmsrkbScKpWMy90DU0BWDLsWkXhTRQ8yItBIWVQViQpZOmOD+V1wqZCoNE0puztkrEKpWF6OmvDJoRkOmZsjCvqL/9lo3zpoqUqEUFIzhsJ1r5xR/yVwj8iRhff44+66wTBY3DAiISYMt/wwaDXb5aDuJutLYJ6uwJfGJWl1qOJW4iiq4NGLSRUKXwdb/QMEPEUjDq9kv5g1A/aQs8LDVcS+bQQASbdojE7IDbfoKdIANyxKx6BEe6NNzELG1jZ/+w7R46/tkg4dGqW0b03Sjqqj4jybW8PlvQq8IgWColMOl7XW405W9nedeuOrP5iUEKb3MGHfrWpaMJRsLOZpJmTgsuwrRAk1v2W7nJz3tzjS1nyrBGKuydDX21Q5h17r99FxH1R5Mv9/AfFRw3RzolHwyVRg3sQG1gaqGUjUKXn65mIKKAUgxRscVdX+P+x6MyGm4+7EkXmxGRRzkC05hL4heyBG9RLBbPI7Ev6dAtIkhdZaOuOEwqr0mfVyjCLW:orSvciapnuJo0Ca7E9LRtLvJRWlZMRttQAhwDVBCqgA=; TAsessionID=363f7709-3a31-4198-951a-94be3c009b11|NEW; _gcl_au=1.1.106579617.1696354064; _gcl_aw=GCL.1696354064.EAIaIQobChMIu4u8qLPagQMVTz4GAB3bqw14EAAYASAAEgKIP_D_BwE; _gcl_dc=GCL.1696354064.EAIaIQobChMIu4u8qLPagQMVTz4GAB3bqw14EAAYASAAEgKIP_D_BwE; _rdt_uuid=1696354064693.0dcd6c3a-655b-483e-88d3-03c57640a6e0; incap_ses_390_2163526=4cX9ML1v6X5h42D0epBpBRBPHGUAAAAA79f8Ip/4mj5HXK3PsSdKuA==; nlbi_2163526=qOC0Ig+1yhoEAPDoB1D/egAAAACUGLYcEr22rEAscDAxyBxT; notice_behavior=implied,eu; visid_incap_2163526=R0D6IWbxQPiwSRS7Y/jZGRBPHGUAAAAAQUIPAAAAAAClVVnHaiedXY+y1vZqJqYq; incap_ses_390_2222183=v9fAc/hETS7p32D0epBpBQ5PHGUAAAAAoH8C+fdQS1xNcdOl1UXF0A==; nlbi_2222183=5gtyAQhMnFDRmxTDUnWprgAAAADZxm4h+HzWyF3AzWBG+iK5; visid_incap_2222183=auOYClrQRtaPTndI66QXvA5PHGUAAAAAQUIPAAAAAABO3B94R5Rixh+GHo4s8ffd',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Host': 'consumerapi.moneygram.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15',
    'Referer': 'https://www.moneygram.com/',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'locale-header': 'fr_FR',
    'clientKey': 'Basic V0VCX2VkYjI0ZDc5LTA0ODItNDdlMi1hNmQ2LTc4ZGY5YzI4MmM0ZTo1MTNlMTEyOS0yZTJmLTRlYmUtYjkwMi02YTVkMGViMDNjZjc=',
}

params = {
    'address': 'Pl. de la Concorde, 75008 Paris, France',
    'searchRadius': '10000',
    'limit': '10',
    'country': 'FR',
    'radiusuom': 'km',
    'amazonCard': 'false',
    'sendMoney': 'false',
    'receiveMoney': 'false',
    'billPayment': 'false',
    'reloadOtherCard': 'false',
    'addToPhone': 'false',
    'payPal': 'false',
    'moneyOrder': 'false',
    'xpressPackage': 'false',
    'purchaseMoneygramCard': 'false',
    'reloadMoneygramCard': 'false',
    'receiveToCard': 'false',
    'expressPayment': 'false',
    'purpose': '',
    'agent': '',
}

all_data = []

# Central points for mainland France
central_points_france = [
    "Pl. de la Concorde, 75008 Paris, France",
    "Tun. du Vieux-Port, Marseille, France",
    "Pl. de la Bourse, 33000 Bordeaux, France",
    "Pl. de la Gare, 59800 Lille, France, France",
    "Pl. de la Gare, 67000 Strasbourg, France, France"
]

domtom_regions = [
    ("Guadeloupe", "GP"),
    ("Martinique", "MQ"),
    ("French Guiana", "GF"),
    ("Réunion", "RE"),
    ("Mayotte", "YT"),
    ("Saint Martin", "MF"),
    ("Saint Barthélemy", "BL"),
    ("Wallis and Futuna", "WF"),
    ("Saint Pierre and Miquelon", "PM"),
    ("French Polynesia", "PF"),
    ("New Caledonia", "NC")
]

# Iterate over central points for mainland France
for address in central_points_france:
    params['address'] = address
    params['country'] = 'FR'
    # Preflight request
    preflight_response = requests.options('https://consumerapi.moneygram.com/services/capi/api/v1/location', params=params, headers=headers)
    # Actual GET request
    response = requests.get(
        'https://consumerapi.moneygram.com/services/capi/api/v1/location',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(response.status_code)
    data_df = pd.json_normalize(response.json()['locations'])
    all_data.append(data_df)

# Iterate over DOM-TOM regions (excluding mainland France which we've already handled)
for region, code in domtom_regions[1:]:
    params['country'] = code
    del params['address']  # Remove the address parameter when querying for DOM-TOM
    # Preflight request
    preflight_response = requests.options('https://consumerapi.moneygram.com/services/capi/api/v1/location', params=params, headers=headers)
    # Actual GET request
    response = requests.get(
        'https://consumerapi.moneygram.com/services/capi/api/v1/location',
        params=params,
        cookies=cookies,
        headers=headers,
    )    
    data_df = pd.json_normalize(response.json()['locations'])
    all_data.append(data_df)

# Combine all data and save as a CSV
final_data = pd.concat(all_data, axis=0).drop_duplicates()  # Drop any duplicate rows
final_data.to_csv(f'MoneyGram/extracts/extract_France_and_DOMTOM_{current_date}.csv', encoding='utf-8-sig', index=False, header=True)
