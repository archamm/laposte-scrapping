import pandas as pd
from bs4 import BeautifulSoup
from deepparse import parser
from tqdm import tqdm
import requests

PATH_HREF = 'JourDeMarche/html/Dept.html'
def scrap_assos_in_one_page(soup, df, address_parser):

    '''
    Get name + Adress  
    
    '''
    names = list(map(lambda x:x.text.replace('\n', '') , soup.find_all("h3", {"class": "card-header text-capitalize"})))
    bodys = list(map(lambda x:x.text, soup.find_all("div", {"class": "card-body"})))
    zip_and_city = list(map(lambda x:x.text.replace('\n', '').replace('à ', ', ').strip(), soup.find_all("div", {"class": "card-footer bg-white"})))

    fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]

    for i in range(len(names)):
        data = bodys[i].split('\n')
        data = [x for x in data if x != '']
       #adress_1 = str(data[1].replace('Adresse : ', '')).replace('None ', '').strip()
        #test = (adress_1, zip_and_city[i])
        #full_adress = zip_and_city[i].strip() if adress_1.lower() in  zip_and_city[i].lower() else adress_1 + zip_and_city[i].strip()
        parse_address = address_parser(zip_and_city[i].replace('à ', '')).to_dict(fields=fields)
        row = [names[i], f'{parse_address["StreetName"]}', parse_address["PostalCode"], parse_address["Municipality"], data[0]]
        df.loc[len(df)] = row
#        print(row)

with open(PATH_HREF, 'r') as f:
    html_text = f.read()
soup = BeautifulSoup(html_text, 'html.parser')
# on rentre les identifiants de connexion
res = []
href_containers = list(map(lambda x:x['href'], soup.find_all('a', href=True)))
df = pd.DataFrame(
    columns=['name',  'adress', 'postal_code', 'town', 'horaires'])
address_parser = parser.AddressParser()

for i in tqdm(range(0, len(href_containers))):
    page = requests.get(href_containers[i])
    soup = BeautifulSoup(page.text, 'html.parser')
    get_towns = soup.find_all('div', {"class": "row"})
    href_containersv2 = get_towns[4].find_all('div', {"class": "col-md-6"})
    href_tows = []
    for i in range(0, len(href_containersv2)):
        href_town = href_containersv2[i].find('a', {"class": 'text-reset text-decoration-none'}, href=True)['href']
        page = requests.get(href_town)
        soup = BeautifulSoup(page.text, 'html.parser')
        scrap_assos_in_one_page(soup, df, address_parser)
  
df.to_csv('JourDeMarche/extract/extrat_JdM_012023.csv', encoding='utf-8-sig', header=True, index=False)
