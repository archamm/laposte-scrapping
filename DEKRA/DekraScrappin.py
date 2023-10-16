import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from deepparse import parser
import requests
import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')



CURRENT_URL = 'https://www.le-code-dekra.fr/salles-d-examen?page='


def scrap_assos_in_one_page(soup,res, df, address_parser):

    '''
    Get name + Adress  
    
    '''
    names = list(map(lambda x:x.text, soup.find_all("div", {"class": "views-field views-field-title"})))
    adresses = list(map(lambda x:x.text, soup.find_all("div", {"class": "views-field views-field-city"})))
    fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
    links = list(map(lambda x:x['href'], soup.find_all("a", {"class": "centre_plus_d_infos_btn"})))

    for i in range(len(names)):
        name = names[i]
        parse_address = address_parser(adresses[i]).to_dict(fields=fields)
        row = [name, f'{parse_address["StreetNumber"]} {parse_address["StreetName"]}', parse_address["PostalCode"], parse_address["Municipality"], links[i]]
        df.loc[len(df)] = row



if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['name',  'adress', 'postal_code', 'town', 'link'])
        

    # on rentre les identifiants de connexion
    res = []
    address_parser = parser.AddressParser()

    for i in tqdm(range(1, 19, 1)):
        print(CURRENT_URL + str(i))
        page = requests.get(CURRENT_URL + str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        scrap_assos_in_one_page(soup, res, df, address_parser)


    df.to_csv(f'DEKRA/extracts/extrat_DEKRA_{current_date}.csv', encoding='utf-8-sig', header=True)
