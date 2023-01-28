import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from deepparse import parser
import requests





PATH = 'DEKRA/response.html'
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

    for i in tqdm(range(1, 16, 1)):
        page = requests.get(CURRENT_URL + str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        scrap_assos_in_one_page(soup, res, df, address_parser)

    with open('DEKRA/extracts/extrat_DEKRA.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
    df.to_csv('DEKRA/extracts/extrat_DEKRA_012023.csv', encoding='utf-8-sig', header=True)
