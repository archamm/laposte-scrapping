import requests
import pandas as pd
from tqdm import tqdm
import json

cookies = {
    'AKCountry': 'FR',
    'AKZip': '',
    'AKRegioncode': 'IDF',
    'AKCity': 'PARIS',
    'AKAreacode': '',
    'AKCounty': '',
    'WUCountryCookie_': 'FR',
    'WULanguageCookie_': 'fr',
    'AK_TLS_Version': 'tls1.2',
    'resolution_height': '800',
    'resolution_width': '1280',
    'is_tablet': 'false',
    'is_mobile': 'false',
    'wu_device_id': '35266993-5b62-0619-80ec-b3bfcfca12b2',
    'A4kgk7nd_dc': '%7B%22c%22%3A%20%22OHk5c3JMMzVKMEREa3htbg%3D%3DTV5nxiNPIvAPpX2qWzBnMCw0sLK9eaBYgmKnYFQCVPKgMIvrWXZRt-rttKfGEYwOezz_n4FJzWwBxT_P5XBRcT4A2HCyQL8jKkpVYO6uXA%3D%3D%22%2C%20%22dc%22%3A%200%2C%20%22mf%22%3A%200%7D',
    'dtCookie': 'v_4_srv_3_sn_6321C416BCDDB86E4602FCEBE9C7D1D5_perc_100000_ol_0_mul_1_app-3A4f296d341a47bdba_0',
    'userCookieOptIn': ",C0001,'",
    'A4kgk7nd': 'A-7c9geJAQAA8xZgA6lsFTQWoAdgby9HAeT64NU_uEl7i5rhijeNKPU9D3jpAZOh6W6uchRAwH8AAEB3AAAAAA|1|1|2d7ba63d36081b240610d4e137f9c199e63830b8',
    'AMCVS_AACD3BC75245B4940A490D4D%40AdobeOrg': '1',
    'CountryCode': 'fr',
    'LangCode': 'fr',
    'AMCV_AACD3BC75245B4940A490D4D%40AdobeOrg': '1430045084%7CMCIDTS%7C19538%7CMCMID%7C61777793992158028246084386876975791202%7CMCAID%7CNONE%7CMCOPTOUT-1688063012s%7CNONE%7CvVersion%7C5.5.0',
    'BIGipServerpool_origin-digital-chi.westernunion.com': '!aYpAaWePDM7HVgMEAvrEqYENwFQi5hWOdFdWL3boL8WfSXiNK3+U+IHQaOYj/A6ucwF/KXjBBOhYnTQ=',
    'bm_sz': 'F28A5D46709B0C207D4006C379614888~YAAQHsARYK6B7t2IAQAAwt5BCxQDxn0MzMCFNj5gx8M/5eb/ZemYCbvICZ1e66U6PzmdL//Po6orN+I0/FCYke+lUyhdzREWQHJH3/k9ckCNntAsVa6zr0xEXboFI6P7PItRqZ2sIzqf0m/wGvoH7uopDlcMcYSUecrTexzA8YgPVYJg3IOLFHSlXCVVsrHtPhgbybRpZ4Oj1sp47J0dsU+X6NqmF6P4uvIPXx9kkQVrpy7ZPsa3o5Ck8FKKFHBivVi0Wotv9yVDKoExrQ6nNI+oeCfRuz9R/vN77tZwkVc3trd3LFD/CkA=~3359795~3684147',
    '_abck': 'E21C27C260C50641EBF7D7D4E9BA6E9A~0~YAAQHsARYLGB7t2IAQAAdt9BCwpEC607OocdGxrmW0ZNyhEeLCi+caB19BqEp9gWx3IDUJoAP75qCsN8qgrKzEjmduHMkDJc8f4Jw4Oyw1zK6AWt+HqCS2zfi3rsAuT5z1XXHjJPMKRYjc9/f4RprnfbSLj/Cxsx041QP5crP5LQotdFC5sjQaiZoRYMIH+gqzFe80X9l9h6qAWAHgc5h1k5muCYO8B+37RH3UNueR4+JN6abEc8wnoLS7VoEvliwTmomp6bYaIUQi1zhGst8sVU1PQ2rb9s65y5nNMyFUbeOHnIAF+Fu+2CDGQUtUqY/BmS3Wb0sARXhXR73LN+vxaCRYEEbiANT/rDFFHVFdqTf0YAuDm1S2AEo/ygbOPBsPs1PFWf6REKCHXVNUwrj680m7IJL1xD0bA/dAjV~-1~-1~1688114576',
    'akavpau_en': '1688111322~id=9671d10268000fc694affbc6d0bce390',
    'ak_bmsc': '64B1DD38281AF5152295B2A057EBCDB0~000000000000000000000000000000~YAAQHsARYO6C7t2IAQAA7v9BCxSjPq9JObaACWjD2DO1psnGkz1lLT6TXV9Fw3oazyDky84v8ON3o2hDeTStyW+qaaGAoWUGZllV2zhJBAYI3wSqQRknK5iYLeqkgjACuLGo7ZvqzK473z9JZz8+TwdeP87IaLvbRw6mx6srUyFn9ScjFY/BUNikaesElbGGol2bWFBB9+z1WgXg9OTW/X4tkZV+mb9R6znosnsCXkdMcff6ZRSCWoE+CpMbteOpqM1dS88VXVNkJbiejrG8XooQnhCi5Irilmw4+tfL9qSbAuIlx2Vqxr4roqEq9uun+SjC+lu8JIcYa8w0JbxNR8nL7DvklGD2Jo82sRjVFMS9QtJmMWzOjZn7KdbVBWPGS5L3Wn7uNMZR/aLexm+hb9U=',
}
 
headers = {
    'authority': 'www.westernunion.com',
    'accept': '*/*',
    'accept-language': 'fr-FR',
    'content-type': 'application/json',
    # 'cookie': "AKCountry=FR; AKZip=; AKRegioncode=IDF; AKCity=PARIS; AKAreacode=; AKCounty=; WUCountryCookie_=FR; WULanguageCookie_=fr; AK_TLS_Version=tls1.2; resolution_height=800; resolution_width=1280; is_tablet=false; is_mobile=false; wu_device_id=35266993-5b62-0619-80ec-b3bfcfca12b2; A4kgk7nd_dc=%7B%22c%22%3A%20%22OHk5c3JMMzVKMEREa3htbg%3D%3DTV5nxiNPIvAPpX2qWzBnMCw0sLK9eaBYgmKnYFQCVPKgMIvrWXZRt-rttKfGEYwOezz_n4FJzWwBxT_P5XBRcT4A2HCyQL8jKkpVYO6uXA%3D%3D%22%2C%20%22dc%22%3A%200%2C%20%22mf%22%3A%200%7D; dtCookie=v_4_srv_3_sn_6321C416BCDDB86E4602FCEBE9C7D1D5_perc_100000_ol_0_mul_1_app-3A4f296d341a47bdba_0; userCookieOptIn=,C0001,'; A4kgk7nd=A-7c9geJAQAA8xZgA6lsFTQWoAdgby9HAeT64NU_uEl7i5rhijeNKPU9D3jpAZOh6W6uchRAwH8AAEB3AAAAAA|1|1|2d7ba63d36081b240610d4e137f9c199e63830b8; AMCVS_AACD3BC75245B4940A490D4D%40AdobeOrg=1; CountryCode=fr; LangCode=fr; AMCV_AACD3BC75245B4940A490D4D%40AdobeOrg=1430045084%7CMCIDTS%7C19538%7CMCMID%7C61777793992158028246084386876975791202%7CMCAID%7CNONE%7CMCOPTOUT-1688063012s%7CNONE%7CvVersion%7C5.5.0; BIGipServerpool_origin-digital-chi.westernunion.com=!aYpAaWePDM7HVgMEAvrEqYENwFQi5hWOdFdWL3boL8WfSXiNK3+U+IHQaOYj/A6ucwF/KXjBBOhYnTQ=; bm_sz=F28A5D46709B0C207D4006C379614888~YAAQHsARYK6B7t2IAQAAwt5BCxQDxn0MzMCFNj5gx8M/5eb/ZemYCbvICZ1e66U6PzmdL//Po6orN+I0/FCYke+lUyhdzREWQHJH3/k9ckCNntAsVa6zr0xEXboFI6P7PItRqZ2sIzqf0m/wGvoH7uopDlcMcYSUecrTexzA8YgPVYJg3IOLFHSlXCVVsrHtPhgbybRpZ4Oj1sp47J0dsU+X6NqmF6P4uvIPXx9kkQVrpy7ZPsa3o5Ck8FKKFHBivVi0Wotv9yVDKoExrQ6nNI+oeCfRuz9R/vN77tZwkVc3trd3LFD/CkA=~3359795~3684147; _abck=E21C27C260C50641EBF7D7D4E9BA6E9A~0~YAAQHsARYLGB7t2IAQAAdt9BCwpEC607OocdGxrmW0ZNyhEeLCi+caB19BqEp9gWx3IDUJoAP75qCsN8qgrKzEjmduHMkDJc8f4Jw4Oyw1zK6AWt+HqCS2zfi3rsAuT5z1XXHjJPMKRYjc9/f4RprnfbSLj/Cxsx041QP5crP5LQotdFC5sjQaiZoRYMIH+gqzFe80X9l9h6qAWAHgc5h1k5muCYO8B+37RH3UNueR4+JN6abEc8wnoLS7VoEvliwTmomp6bYaIUQi1zhGst8sVU1PQ2rb9s65y5nNMyFUbeOHnIAF+Fu+2CDGQUtUqY/BmS3Wb0sARXhXR73LN+vxaCRYEEbiANT/rDFFHVFdqTf0YAuDm1S2AEo/ygbOPBsPs1PFWf6REKCHXVNUwrj680m7IJL1xD0bA/dAjV~-1~-1~1688114576; akavpau_en=1688111322~id=9671d10268000fc694affbc6d0bce390; ak_bmsc=64B1DD38281AF5152295B2A057EBCDB0~000000000000000000000000000000~YAAQHsARYO6C7t2IAQAA7v9BCxSjPq9JObaACWjD2DO1psnGkz1lLT6TXV9Fw3oazyDky84v8ON3o2hDeTStyW+qaaGAoWUGZllV2zhJBAYI3wSqQRknK5iYLeqkgjACuLGo7ZvqzK473z9JZz8+TwdeP87IaLvbRw6mx6srUyFn9ScjFY/BUNikaesElbGGol2bWFBB9+z1WgXg9OTW/X4tkZV+mb9R6znosnsCXkdMcff6ZRSCWoE+CpMbteOpqM1dS88VXVNkJbiejrG8XooQnhCi5Irilmw4+tfL9qSbAuIlx2Vqxr4roqEq9uun+SjC+lu8JIcYa8w0JbxNR8nL7DvklGD2Jo82sRjVFMS9QtJmMWzOjZn7KdbVBWPGS5L3Wn7uNMZR/aLexm+hb9U=",
    'isrrenabled': 'false',
    'origin': 'https://www.westernunion.com',
    'platform': 'nextgen',
    'referer': 'https://www.westernunion.com/global-services/find-locations?WUCountry=fr&WULanguage=fr',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'wucountrycode': 'FR',
    'wulanguagecode': 'fr',
    'x-wu-accesscode': 'RtYV3XDz9EA',
    'x-wu-operationname': 'locations',
}
 
json_data = {
    'query': 'query  locations( $req:LocationInput, ) { locations(input: $req) }',
    'variables': {
        'req': {
            'longitude': '2.24555203692713',
            'latitude': '48.88995306438624',
            'country': 'FR',
            'openNow': '',
            'services': [],
            'sortOrder': 'Distance',
            'pageNumber': '1',
        },
    },
}
 
res = []


data = pd.read_csv('WesternUnion/dom_tom_coordinates.csv')





res = []
# on rentre les identifiants de connexion
data = data.reset_index()  # make sure indexes pair with number of rows
with tqdm(total=data.shape[0]) as pbar:    
    for index, row in data.iterrows():
        if row['Latitude'] and row['Longitude']:
            json_data['variables']['req']['latitude'] = str(row['Latitude'])
            json_data['variables']['req']['longitude'] = str(row['Longitude'])
            for i in range(1, 11):
                json_data['variables']['req']['pageNumber'] = str(i)
                response = requests.post('https://www.westernunion.com/router/', cookies=cookies, headers=headers, json=json_data)
                if response.status_code != 200:
                    print(response.status_code)
                    print(str(row['Latitude']) + ' ' +  str(row['Longitude']))
                try:
                    res.append(response.json())
                except Exception:
                    print('Error parsing json on ' + str(row['latitude']) + ', ' +  str(row['longitude']))
        pbar.update(1)

            
    


with open('WesternUnion/extracts/extract_WesternUnion_dom_tom_0723.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"countryTo":"FR","findLocationType":"RMT","lat":"","latitude":48.83630226833469,"long":"","longitude":2.3115479999999025,"PayAgentId":null,"RequestCountry":"US","RequiredPayoutAgents":false,"RequiredReceivingAgents":false,"RequiredReceivingAndPayoutAgents":false}'
#response = requests.put('https://public.riamoneytransfer.com/location/agent-locations', headers=headers, data=data)