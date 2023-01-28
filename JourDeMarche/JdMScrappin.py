import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from deepparse import parser
from tqdm import tqdm
import re

CURRENT_URL = 'https://www.jours-de-marche.fr/recherche/?idLieu='

def find_between(str, start, end):
    result = re.search(f'{start}(.*){end}', str)
    return result.group(1)

def scrap_assos_in_one_page(soup, df, address_parser):

    '''
    Get name + Adress  
    
    '''
    names = list(map(lambda x:x.text.replace('\n', '') , soup.find_all("h3", {"class": "card-header text-capitalize"})))
    bodys = list(map(lambda x:x.text, soup.find_all("div", {"class": "card-body"})))
    zip_and_city = list(map(lambda x:x.text.replace('\n', '') , soup.find_all("div", {"class": "card-footer bg-white"})))

    fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]

    for i in range(len(names)):
        data = bodys[i].split('\n')
        data = [x for x in data if x != '']
        adress_1 = str(data[1].replace('Adresse : ', '')).replace('None ', '').strip()
        test = (adress_1, zip_and_city[i])
        full_adress = zip_and_city[i].strip() if adress_1.lower() in  zip_and_city[i].lower() else adress_1 + zip_and_city[i].strip()
        parse_address = address_parser(full_adress.replace('à ', ', ').strip()).to_dict(fields=fields)
        row = [names[i], f'{parse_address["StreetName"]}', parse_address["PostalCode"], parse_address["Municipality"], data[0]]
        df.loc[len(df)] = row
        print(row)


if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['name',  'adress', 'postal_code', 'town', 'horaires'])
    address_parser = parser.AddressParser()

    for i in tqdm(range(1, 38000, 1)):
        page = requests.get(CURRENT_URL + str(i))

        if ('Nous croyons fortement au développement de la vie locale sous tous ses aspects.' in page.text): 
            continue
        print(CURRENT_URL + str(i))

        soup = BeautifulSoup(page.text, 'html.parser')
        scrap_assos_in_one_page(soup, df, address_parser)


    df.to_csv('JourDeMarche/extract/extrat_JdM_012023.csv', encoding='utf-8-sig', header=True, index=False)