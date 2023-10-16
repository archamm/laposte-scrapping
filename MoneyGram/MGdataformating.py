import json
from tqdm import tqdm
import pandas as pd
import requests
import datetime
import os

current_date = datetime.datetime.now().strftime('%Y%m%d')

import requests

cookies = {
    'IR_16828': '1696689359635%7C0%7C1696689359635%7C%7C',
    '_fbp': 'fb.1.1696689365917.1635495431',
    '_ga': 'GA1.2.953415560.1696689359',
    '_ga_419TZ53GJ4': 'GS1.1.1696689359.1.1.1696689368.0.0.0',
    '_gid': 'GA1.2.1479239129.1696689365',
    '_gat_UA-42673143-1': '1',
    '_rdt_uuid': '1696689361019.3f41dee8-a4cf-4c9a-9c3e-75586816cd57',
    'IR_gbd': 'moneygram.com',
    'incap_ses_392_2163526': 'h8qXJF29hgl63Rka+KpwBc5sIWUAAAAACKo6LhXBGhKSTWniE1x0tA==',
    'nlbi_2163526': 'XXzhcMnJuXpBLoWZB1D/egAAAABJZYuYZa1jR0T1vYgDMuq4',
    '_gcl_au': '1.1.271681291.1696689356',
    'cmapi_cookie_privacy': 'permit 1,2,3,4',
    'cmapi_gtm_bl': '',
    'nlbi_2222183_2147483392': 'cQ0sC9R2o31DYEVCUnWprgAAAAD+J5T3iBPQva35DXEtKDgn',
    'notice_gdpr_prefs': '0,1,2,3:',
    'notice_preferences': '3:',
    'reese84': '3:hpxSSLW8JjpA2VNTvti7XQ==:OJbpcsNqJZxvXjJgkj/uQO/8HxrrJf4Oepw8uIZk9HoDMWYyY4UyIKQnS2819eCrelQoSczZjOFiiTW2g6FyMwXlThGWv6EEsu/w+lqPujd6N+iVmVgOx2W3PpEtbbM9AUB66oStBSNa4JT1sZNzV+d7y2jg1SLxvwktFuuwaBPFl4zcqHoazTWXszafCJL9vf5XXYW39Qg1LAG6k6ccpTI6Hz9a6RwNHWWMtXNYAKwBjWbkUdEBofScEJQHf1L2kF+4/1ElsZDKCvai2z7ADYUgQono3e56tMHe1Gzszy8QmA7ARJViG+A1Zi4gSDd1FbLoXg5hN7dVNQSHf/6lzNiIaj3RgmWi6+jgrz5OzFvmM555R+5duIl/PCqzdqy2bt43KJwOuqUGqseJIRDV0PMW7vX+UK0/To023eXtSn1eXNc6hRYWZP8A8aRrjlQB8oSXfcCihIzGoAgPyhh/xOY093lVBcqAH7E7eMeInJ0=:AV8c4ovIFvqpK6y0bkoxV0tAIq9UbrAwaP7mUjAQzHg=',
    'TAsessionID': '15d5febd-b63c-4a7b-aaad-dc6ed960be0f|NEW',
    'notice_behavior': 'implied,eu',
    'visid_incap_2222183': 'auOYClrQRtaPTndI66QXvA5PHGUAAAAAQkIPAAAAAACAi32vAVnPq6V7N3Z985TiMK+/Hjw8CX8l',
    'nlbi_2222183': 'W2XtSZm0o2AYR4xpUnWprgAAAADr+qxc+hKP4J+zS5l2OROr',
    'incap_ses_392_2222183': 'cuTqSztSb3i29RYa+KpwBRZqIWUAAAAA5UnbhjM9SIKMLri8R/o+0w==',
    'visid_incap_2163526': 'R0D6IWbxQPiwSRS7Y/jZGRBPHGUAAAAAQUIPAAAAAAClVVnHaiedXY+y1vZqJqYq',
}

headers = {
    'Accept': 'application/json',
    'Origin': 'https://www.moneygram.com',
    # 'Cookie': 'IR_16828=1696689359635%7C0%7C1696689359635%7C%7C; _fbp=fb.1.1696689365917.1635495431; _ga=GA1.2.953415560.1696689359; _ga_419TZ53GJ4=GS1.1.1696689359.1.1.1696689368.0.0.0; _gid=GA1.2.1479239129.1696689365; _gat_UA-42673143-1=1; _rdt_uuid=1696689361019.3f41dee8-a4cf-4c9a-9c3e-75586816cd57; IR_gbd=moneygram.com; incap_ses_392_2163526=h8qXJF29hgl63Rka+KpwBc5sIWUAAAAACKo6LhXBGhKSTWniE1x0tA==; nlbi_2163526=XXzhcMnJuXpBLoWZB1D/egAAAABJZYuYZa1jR0T1vYgDMuq4; _gcl_au=1.1.271681291.1696689356; cmapi_cookie_privacy=permit 1,2,3,4; cmapi_gtm_bl=; nlbi_2222183_2147483392=cQ0sC9R2o31DYEVCUnWprgAAAAD+J5T3iBPQva35DXEtKDgn; notice_gdpr_prefs=0,1,2,3:; notice_preferences=3:; reese84=3:hpxSSLW8JjpA2VNTvti7XQ==:OJbpcsNqJZxvXjJgkj/uQO/8HxrrJf4Oepw8uIZk9HoDMWYyY4UyIKQnS2819eCrelQoSczZjOFiiTW2g6FyMwXlThGWv6EEsu/w+lqPujd6N+iVmVgOx2W3PpEtbbM9AUB66oStBSNa4JT1sZNzV+d7y2jg1SLxvwktFuuwaBPFl4zcqHoazTWXszafCJL9vf5XXYW39Qg1LAG6k6ccpTI6Hz9a6RwNHWWMtXNYAKwBjWbkUdEBofScEJQHf1L2kF+4/1ElsZDKCvai2z7ADYUgQono3e56tMHe1Gzszy8QmA7ARJViG+A1Zi4gSDd1FbLoXg5hN7dVNQSHf/6lzNiIaj3RgmWi6+jgrz5OzFvmM555R+5duIl/PCqzdqy2bt43KJwOuqUGqseJIRDV0PMW7vX+UK0/To023eXtSn1eXNc6hRYWZP8A8aRrjlQB8oSXfcCihIzGoAgPyhh/xOY093lVBcqAH7E7eMeInJ0=:AV8c4ovIFvqpK6y0bkoxV0tAIq9UbrAwaP7mUjAQzHg=; TAsessionID=15d5febd-b63c-4a7b-aaad-dc6ed960be0f|NEW; notice_behavior=implied,eu; visid_incap_2222183=auOYClrQRtaPTndI66QXvA5PHGUAAAAAQkIPAAAAAACAi32vAVnPq6V7N3Z985TiMK+/Hjw8CX8l; nlbi_2222183=W2XtSZm0o2AYR4xpUnWprgAAAADr+qxc+hKP4J+zS5l2OROr; incap_ses_392_2222183=cuTqSztSb3i29RYa+KpwBRZqIWUAAAAA5UnbhjM9SIKMLri8R/o+0w==; visid_incap_2163526=R0D6IWbxQPiwSRS7Y/jZGRBPHGUAAAAAQUIPAAAAAAClVVnHaiedXY+y1vZqJqYq',
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
    'searchRadius': '100000000',
    'limit': '100000000000',
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

response = requests.get(
    'https://consumerapi.moneygram.com/services/capi/api/v1/location',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.json())
'''
with open("MoneyGram\extract_raw_MG_0123.json", "r") as f:
        decoded_data=f.readline().encode().decode('utf-8-sig') 
        data = json.loads(decoded_data)
'''
data_df = pd.json_normalize(response.json()['locations'])


file_path = f'MoneyGram/extracts/extract__{current_date}.csv'

# If the file already exists, we'll append without the header
if os.path.exists(file_path):
    data_df.to_csv(file_path, mode='a', encoding='utf-8-sig', index=False, header=False)
else:
    # Otherwise, we'll create the file with the header
    data_df.to_csv(file_path, encoding='utf-8-sig', index=False, header=True)
