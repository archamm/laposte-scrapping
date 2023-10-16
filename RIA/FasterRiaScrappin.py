import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import json
import pandas as pd
from tqdm import tqdm
import time
from concurrent.futures import ThreadPoolExecutor

def get_new_session_token(): 

    headers_session = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'CultureCode': 'en-US',
        'IsoCode': 'US',
        'Origin': 'https://app.riamoneytransfer.com',
        'Referer': 'https://app.riamoneytransfer.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    return 'Bearer ' + requests.get('https://public.riamoneytransfer.com/Authorization/session', headers=headers_session).json()['authToken']['jwtToken']

def fetch_location(row):
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    json_data = {
        'countryTo': 'FR',
        'findLocationType': 'RMT',
        'lat': '',
        'latitude': row.latitude,
        'long': '',
        'longitude': row.longitude,
        'PayAgentId': None,
        'RequestCountry': 'US',
        'RequiredPayoutAgents': False,
        'RequiredReceivingAgents': False,
        'RequiredReceivingAndPayoutAgents': False,
    }
    
    headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImN0eSI6IkpXVCJ9.eyJqdGkiOiJlOWRmYTUwZC0xZWYxLTQyODItOWE4MC1mMDliMTQ2OGYxZTQiLCJpYXQiOjE2NzQ5MDIyMDUsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL25hbWUiOiI5MC41OS43NC4xOTciLCJhcGlUb2tlbiI6ImV5SmhiR2NpT2lKSVV6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpxZEdraU9pSmlaVFl3TkdReU5TMDBNamczTFRSa09UUXRZbVl3WmkweVltUTNaVEl3WmpsbFpUVWlMQ0pwWVhRaU9qRTJOelE1TURJeU1EVXNJa05zYVdWdWRGUjVjR1VpT2lKWFpXSWlMQ0pEYkdsbGJuUkpjRUZrWkhKbGMzTWlPaUk1TUM0MU9TNDNOQzR4T1RjaUxDSm9kSFJ3T2k4dlEzVnpkRzl0WlhKVFpYSjJhV05sVkc5dmJHdHBkQzV5YVdGbGJuWnBZUzV1WlhRdmFXUmxiblJwZEhrdlkyeGhhVzF6TDFObGMzTnBiMjVKUkNJNklqVXdNREEyTmpZME5qRXlPU0lzSW5WdWFYRjFaVjl1WVcxbElqb2lVbWxoUVZCSklpd2lZWFYwYUY5MGFXMWxJam9pTVM4eU9DOHlNREl6SURFd09qTTJPalEwSUVGTklpd2lZWFYwYUcxbGRHaHZaQ0k2SW1oMGRIQTZMeTl6WTJobGJXRnpMbTFwWTNKdmMyOW1kQzVqYjIwdmQzTXZNakF3T0M4d05pOXBaR1Z1ZEdsMGVTOWhkWFJvWlc1MGFXTmhkR2x2Ym0xbGRHaHZaQzl3WVhOemQyOXlaQ0lzSWtGblpXNTBRWEJwVlhObGNtNWhiV1VpT2lKU2FXRkJVRWtpTENKU1pXTmxhWFpwYm1kQloyVnVkRWxrSWpvaU1UQTVOREF4TWlJc0lrRnNiRzkzUlcxaGFXeFRaVzVrYVc1bklqb2lkSEoxWlNJc0lrRnNiRzkzU1hCQlpHUnlaWE56Vlc1aWJHOWphMmx1WnlJNkluUnlkV1VpTENKQmJHeHZkMDl5WkdWeVRHOXZhM1Z3Y3lJNkluUnlkV1VpTENKdVltWWlPakUyTnpRNU1ESXlNRFFzSW1WNGNDSTZNVFkzTkRrd05UZ3dOQ3dpYVhOeklqb2ljMlZ6YzJsdmJpQnBjM04xWlhJaUxDSmhkV1FpT2lKb2RIUndPaTh2YzJWemMybHZiaTUwZENKOS5lVm16YXl1YzhhUVoycUw1ZURCamJueHNWb18wYmlhM0xoek4xU2oxLUxzIiwicm10RW1haWwiOiI5MC41OS43NC4xOTciLCJzZXNzaW9uQ2FjaGVLZXkiOiJkYThkNDhlNy1hYzc2LTQzMmMtYmFlNS03YjI4Nzk0YmYxZGEiLCJpcElzb0NvZGUiOiJGUiIsImNsaWVudElwQWRkcmVzcyI6IjkwLjU5Ljc0LjE5NyIsInRva2VuVHlwZSI6InB1YmxpY19zZXNzaW9uIiwiY2xpZW50VHlwZSI6IldlYiIsIkJyYW5kIjoiMCIsImlzb0NvZGUiOiJVUyIsInNlc3Npb25DdWx0dXJlQ29kZSI6ImVuLVVTIiwiY3VsdHVyZUNvZGUiOiJlbi1VUyIsIlNlc3Npb25JZCI6IjUwMDA2NjY0NjEyOSIsImF1ZCI6WyJSTVRXZWIiLCJDU1QiXSwibmJmIjoxNjc0OTAyMjA1LCJleHAiOjE2NzQ5MDM0MDUsImlzcyI6IkF1dGhTZXJ2ZXIifQ.ejvdwn5qTWXWaUCwmKjhpKm5dQWI69v_hzxzn815sB8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'CultureCode': 'en-US',
    'IsoCode': 'US',
    'Origin': 'https://app.riamoneytransfer.com',
    'Referer': 'https://app.riamoneytransfer.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}


    
    response = requests.put('https://public.riamoneytransfer.com/location/agent-locations', headers=headers, json=json_data)
    if response.status_code == 500:
        headers['Authorization'] = get_new_session_token()
        response = requests.put('https://public.riamoneytransfer.com/location/agent-locations', headers=headers, json=json_data)

    try:
        return response.json()
    except Exception as e:
        print(f'Error parsing json on {row.latitude}, {row.longitude}: {e}')

def main():
    data = pd.read_csv('RIA/communes-departement-region.csv')
    data = data[data['latitude'].notnull() & data['longitude'].notnull()]  # Filter out rows with null lat/long
    
    with ThreadPoolExecutor(max_workers=5) as executor:  # Limit to 5 concurrent workers
        res = list(tqdm(executor.map(fetch_location, data.itertuples(index=False)), total=len(data)))
    
    with open('RIA/extract/extrat_RIA_1023.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False)

if __name__ == "__main__":
    main()
