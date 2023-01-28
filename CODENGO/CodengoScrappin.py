import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

from deepparse import parser






PATH = 'CODENGO/responseCODENGO0103.html'



def scrap_assos(container,res, df, address_parser):

    '''
    Get name + Adress  
    
    '''
    data = list(map(lambda x:" ".join(x.split()), container.text.split('\n')))
    name = " ".join(data[1].split())
    adress = " ".join(data[2].split())
    ville = " ".join(data[3].split()).split(' ')[1]
    code_postal = " ".join(data[3].split()).split(' ')[0]


    try:
        fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
        parse_address = address_parser(f'{data[2]} {data[3]}').to_dict(fields=fields)
        row = [name, f'{parse_address["StreetNumber"]} {parse_address["StreetName"]}', parse_address["PostalCode"], parse_address["Municipality"]]
        print(row)
    except Exception:
        row = [name, adress, code_postal, ville]
    df.loc[len(df)] = row



if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['name',  'adress', 'postal_code', 'town'])
        
    with open(PATH, 'r') as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text, 'html.parser')
    # on rentre les identifiants de connexion
    res = []
    containers = soup.find_all("li", {"class": "col3 site ng-binding ng-scope"})
    print(len(containers))
    address_parser = parser.AddressParser()
    for i in tqdm(range(len(containers))):
            scrap_assos(containers[i], res, df, address_parser)

    with open('CODENGO/extract/extrat_CODENGO.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
    df.to_csv('CODENGO/extract/extrat_CODENGO_012023.csv', encoding='utf-8-sig', header=True, index=False)
