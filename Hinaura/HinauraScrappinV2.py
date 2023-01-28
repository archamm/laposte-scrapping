import json
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from AdresseParser import AdresseParser
import re
import validators


warnings.filterwarnings("ignore", category=DeprecationWarning)


PATH = '/Users/matthieuarchambault/Documents/projetPerso/PosteScrappin/Hinaura/response.html'
CURRENT_URL = 'https://carto.hinaura.fr/?BaseRegionaleAnnuaire'

def check_if_number(number):
    
    regex = '^(?:(?:\+|00)33[\s.-]{0,3}(?:\(0\)[\s.-]{0,3})?|0)[1-9](?:(?:[\s.-]?\d{2}){4}|\d{2}(?:[\s.-]?\d{3}){2})$'
    # pass the regular expression
    # and the string into the fullmatch() method
    return re.fullmatch(regex, number)

def check_if_email(email):
    
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    return re.fullmatch(regex, email)
 
 


def scrap_assos(container,res, df):

    '''
    Get relevent Adress and other available contact information from the div class=col-sm-6  
    
    '''
    adr_parser = AdresseParser()
    name = container.find('h2').text
    infos = container.find("div", {"class": "col-sm-6"})
    data = list(map(lambda x:x.text.replace('\n', ''), infos.find_all('p')))
    adress = f'{data[0]} {data[1]}'
    try:
        result = adr_parser.parse(" ".join(adress.split()))
        ville = result['ville']['nom']
        code_postal = result['code_postal']
    except Exception:
        code_postal = ''
        ville = ''
    number = ''
    email = ''
    website = ''

    for item in data[1:]:
        item = item.replace(' ', '')
        if (check_if_email(item)):
            email = item
        elif (check_if_number(item)):
            number = item
        elif (validators.url(item)):
            website = item


  
    

    '''
    Get target profiles & prices
    '''

    targets = []
    tarif = []
    target_container = container.find_all("div", {"class": "panel panel-success"})

    for item in target_container:
        try:
            if('Publics' in item.text.replace('\n', '')):
                targets = list(map(lambda x:x.text.replace('\n', ''), item.find_all('li')))
            elif('Tarifs' in item.text.replace('\n', '')):
                tarif = list(map(lambda x:x.text.replace('\n', ''), item.find_all('li')))

        except AttributeError:
            print('Error in target div for ' + name)


    '''
        Get services 
    '''
    basic_skills_support = []
    understand_rights_sites = []
    digital_culture_awareness = []
    target_container = container.find_all("div", {"class": "panel panel-primary"})

    for item in target_container:
        try:
            if('Accompagnement' in item.text.replace('\n', '')):
                basic_skills_support = list(map(lambda x:x.text.replace('\n', ''), item.find_all('li')))
            elif('Comprendre' in item.text.replace('\n', '')):
                understand_rights_sites = list(map(lambda x:x.text.replace('\n', ''), item.find_all('li')))
            elif('Sensibilisations' in item.text.replace('\n', '')):
                digital_culture_awareness = list(map(lambda x:x.text.replace('\n', ''), item.find_all("div", {"class": "picto-modalite"})))
        except AttributeError:
            print('Error in subdiv for ' + name)



    res.append({'nom' : name, 'adresse' : adress, 'postal_code': code_postal, 'town': ville,
     'email': email, 'site_web': website,'number': number,
     'target_audience': targets,'tarifs': tarif, 'basic_skills_support': basic_skills_support, 
     'understand_rights_sites': understand_rights_sites, 'digital_culture_awareness': digital_culture_awareness, 
      })
    row = [name, adress, code_postal, ville, email, website, number]
  
    df.loc[len(df)] = row



if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['name',  'adress', 'postal_code', 'town',
        'email', 'website', 'number'])
        
    with open(PATH, 'r') as f:
        html_text = f.read()
    soup = BeautifulSoup(html_text, 'html.parser')
    # on rentre les identifiants de connexion
    res = []
    containers = soup.find_all("div", {"class": "BAZ_cadre_fiche id8"})
    print(len(containers))
    for i in tqdm(range(len(containers))):
            scrap_assos(containers[i], res, df)

    print(res)
    with open('Hinaura/extract/extrat_Hinaura.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
    df.to_csv('Hinaura/extract/extrat_Hinaura_V2.csv', encoding='utf-8-sig', header=True)

    '''target_audience', 'tarifs', "basic_skills_support", 'understand_rights_sites',
        'digital_culture_awareness'])'''