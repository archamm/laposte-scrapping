from ast import Try
import json
import pandas as pd
from tqdm import tqdm
from deepparse import parser
import requests
from requests.structures import CaseInsensitiveDict
import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')


REQUEST_URL = 'https://exacode.fr/api/sessions/findces?latitude=50.6138111&longitude=3.0423599&earliest=2022-08-31'
PATH = 'ConseillersNumériques/geolocation.json'

CENTRE_URL = 'https://api.conseiller-numerique.gouv.fr/conseillers/permanence/'

def scrap_results(centre, df, address_parser):
    centre_id = centre['properties']['id']
    center_coordinates = centre['geometry']['coordinates']
    centre_nom = centre['properties']['name']
    try :
        centre_isLabeledAidantsConnect = centre['properties']['isLabeledAidantsConnect']
        centre_isLabeledFranceServices = centre['properties']['isLabeledFranceServices']
    except KeyError:
        centre_isLabeledAidantsConnect = False
        centre_isLabeledFranceServices = False
    try:
        centre_openingHours = centre['properties']['openingHours']
    except KeyError:
        centre_openingHours = ''
    adress = centre['properties']['address']
    fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
    parse_address = address_parser(adress).to_dict(fields=fields)
    centre_adress = f'{parse_address["StreetNumber"]} {parse_address["StreetName"]}'
    centre_postal_code = parse_address["PostalCode"]
    centre_town = parse_address["Municipality"]
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    page = requests.get(CENTRE_URL + centre_id)
    data = page.json()
    for conseiller in data['cnfs']:
        row = [conseiller['prenom'], conseiller['nom'], conseiller.get("phone", ''), conseiller.get("email", ''), centre_id , center_coordinates, centre_nom, 
        centre_isLabeledAidantsConnect, 
        centre_isLabeledFranceServices, centre_adress, centre_postal_code, centre_town, centre_openingHours]
        df.loc[len(df)] = row
 
    
if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['prenom', 'nom', 'numero', 'email', 'centre_id' , 'center_coordinates', 'centre_nom', 'centre_isLabeledAidantsConnect', 
        'centre_isLabeledFranceServices', 'centre_adress', 'centre_postal_code', 'centre_town', 'centre_openingHours'])
    f = open(PATH)
    data = json.load(f)
    address_parser = parser.AddressParser()
    number_of_errors = 0
    for i in tqdm(range(len(data['features']))):
        try :
            scrap_results(data['features'][i], df, address_parser)
        except Exception: 
            print('issues on ' + data['features'][i]['properties']['id'])
            number_of_errors += 1

    print('number of errors is ' + str(number_of_errors))

    df.to_csv('ConseillersNumériques/extract/extract_CN.csv', encoding='utf-8-sig', header=True, sep=';')
    


