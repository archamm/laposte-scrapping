import json
from AdresseParser import AdresseParser
from tqdm import tqdm
import pandas as pd
from deepparse import parser



with open("LesBonClics/extrat_lesbonsclics.json", "r") as f:
        data = json.load(f)



df = pd.DataFrame(
        columns=['id', 'nom',  'adresse', 'code_postal', 'ville', 'derniere_modification', 'email', 'site_web', 'numero'])
address_parser = parser.AddressParser()
errors = 0
for i in tqdm(range(len(data))):
    element = data[i]
    try:
        fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
        parse_address = address_parser(element['Adresse']).to_dict(fields=fields)
        row = [element['id'], element["nom"], f'{parse_address["StreetNumber"]} {parse_address["StreetName"]}', parse_address["PostalCode"], parse_address["Municipality"], element['Dernière modification'], element['Email'],
        element["Site Web"], element['Numéro']]
    except Exception:
        row = [element['id'], element["nom"], element['Adresse'], '', '', element['Dernière modification'], element['Email'],
        element["Site Web"], element['Numéro']]
    df.loc[len(df)] = row
print(f'errors in postal codes: {errors}')

df.to_csv('extrat_lesbonsclics_GEOV2.csv',encoding='utf-8-sig', index=False, header=True)