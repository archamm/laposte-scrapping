import json
from os import link
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from deepparse import parser
import requests





CURRENT_URL = 'https://www.pointcode.fr/centres-dexamen/?liste='


def scrap_assos_in_one_page(soup,res, df, address_parser):

    '''
    Get name + Adress  
    '''
    names = list(map(lambda x:x.text, soup.find_all("h2")))
    adresses = list(map(lambda x:x.text, soup.find_all("p")))
    link_centre = list(map(lambda x:x['href'],soup.find_all("a", {"title": "Réserver un examen du code au centre"})))
    print(len(link_centre))
    fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
    print(link_centre)
    names.remove('Nos centres sans rendez-vous !')

    for i in range(0, len(names), 1):
        name = names[i]

        parse_address = address_parser(adresses[i+1].split("Tél : ")[0]).to_dict(fields=fields)
        number = adresses[i+1].split("Tél : ")[1].split("Du ")[0].split("Le ")[0].split("Sur ")[0].split("Mardi ")[0].split("du ")[0].split("Lundi ")[0]
        row = [name, f'{parse_address["StreetNumber"]} {parse_address["StreetName"].replace("-", "")}', parse_address["PostalCode"],
         parse_address["Municipality"], number, link_centre[i]]
        print(row)
        df.loc[len(df)] = row
    '''
    list_centre = soup.find("ul", {"class": "liste-centres"})
    print(len(list_centre.find_all("li")))
    '''

if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['name',  'adress', 'postal_code', 'town', 'number', 'link'])
        

    # on rentre les identifiants de connexion
    res = []
    address_parser = parser.AddressParser()
    for i in tqdm(range(1, 37, 1)):
        page = requests.get(CURRENT_URL + str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        scrap_assos_in_one_page(soup, res, df, address_parser)

    with open('POINTCODE/extracts/extrat_POINTCODE012023.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
    df.to_csv('POINTCODE/extracts/extrat_POINTCODE_012023.csv', encoding='utf-8-sig', header=True)
