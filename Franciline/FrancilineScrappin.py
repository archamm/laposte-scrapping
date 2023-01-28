import json
from time import sleep
import warnings
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from tqdm import tqdm
from deepparse import parser
import re
from urllib.parse import urlparse

warnings.filterwarnings("ignore", category=DeprecationWarning)


option = webdriver.ChromeOptions()
option.add_argument("— incognito")
option.add_argument("--window-size=1440,1000")

option.add_argument("--start-maximized")

option.add_argument('--headless') # permet d'afficher ou non le navigateur et ce qu'effectue commme actions le programme
option.add_argument('--no-sandbox')
CHROME_PATH = r'/usr/local/bin/ls'  # path from 'which chromedriver'

BROWSER = webdriver.Chrome(chrome_options=option)
CURRENT_URL = 'https://carto.francilin.fr/structures/'


def wait_for_element_to_appear(xpath):
    timeout = 20
    # on attends que s'affiche un élément de la page pour continuer
    try:
        WebDriverWait(BROWSER, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        print("Timed out waiting for page to load")
        BROWSER.quit()

def change_page(url):
    BROWSER.get(url)
    BROWSER.refresh()


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
 
 
def check_if_website(email):
    
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def parse_essential_infos(str, services):
    exclude = ['https://carto.francilin.fr/']
    if(str in exclude):
        return
    if(check_if_email(str)):
        services['email'] = str.replace('mailto:', '')
    elif(check_if_number(str.replace('tel:', ''))):
        services['number'] = str    


def click_button(xpath):
    BROWSER.find_element("xpath", xpath).click()

def parse_list(element, services):
    calc = element.text.split('\n')
    services[calc[0]] = calc[1:]

def parse_specs_list(str, services):
    labels_check = ['Pass Numérique', 'Aptic', 'France Services', 'Aidants Connect', 'Conseillers numériques']
    accesibilite_check = ['Accès pour les personnes à mobilité réduite']
    horaires_check = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    accompagnement_check = ['Avec de l’aide', 'À ma place', 'Dans un atelier']

    if any(substring in str for substring in labels_check):
        services['Labels'] = str.split('\n')
    elif any(substring in str for substring in accompagnement_check):
        services['Accompagnement'] = str.split('\n')
    elif any(substring in str for substring in horaires_check):
        services['Horaires'] = str.split('\n')
    elif any(substring in str for substring in accesibilite_check):
        services['Accessibilité'] = str.split('\n')
    


def scrap_assos(id, df, address_parser):


    try:
        name = BROWSER.find_element("xpath",'/html/body/div/div[1]/div[3]/div/div/div[1]/header/h1').text
    except Exception:
        return

    last_modification = ''
    raw_adress = ''
    parse_address = {}
    try:
        last_modification = BROWSER.find_element("xpath",'/html/body/div/div[1]/div[3]/div/div/div[1]/header/p[1]').text.replace('Fiche mise à jour le ', '')
    except Exception:
        print(f'{id} has no last mod')

    services = {}
    elems = BROWSER.find_elements("xpath", "//a[@href]")
    for elem in elems:
        parse_essential_infos(elem.get_attribute("href"), services)

    try:
        raw_adress = BROWSER.find_element("xpath",'/html/body/div/div[1]/div[3]/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div[1]/address').text 
        fields = ["StreetNumber", "StreetName", "Municipality", "Province", "PostalCode"]
        parse_address = address_parser(raw_adress).to_dict(fields=fields)
    except Exception:
        print(f'{id} has no adress')

    for element in BROWSER.find_elements(By.CLASS_NAME,'service-group.mb-4.svelte-6e8z5b'):
        try:
            parse_list(element, services)
        except:
            print(f'{id} has no services')
    for element in BROWSER.find_elements(By.CLASS_NAME,'list-disc.list-inside') + BROWSER.find_elements(By.CLASS_NAME,'list-disc.list-inside.ms-4') + BROWSER.find_elements(By.CLASS_NAME,'item-content.list-disc list-inside.svelte-putgjp'):
        parse_specs_list(element.text, services)
    


    row = [id, name, f'{parse_address["StreetNumber"]} {parse_address["StreetName"]}', parse_address["PostalCode"], parse_address["Municipality"],
    last_modification,
    services.get("email", ''),
    services.get("number", ''),
    services.get("La recherche d'un emploi", ''),
    services.get("Les déclarations en ligne (E-admin)", ''), 
    services.get("Les premiers pas sur internet et en informatique", ''), 
    services.get("L'utilisation des outils bureautiques", ''), 
    services.get("L'approfondissement du numérique", ''), 
    services.get("Des conseils sur la parentalité numérique", ''), 
    services.get("Des usages professionnels sur informatique", ''), 
    services.get("L'utilisation d'outils créatifs", ''), 
    services.get("Labels", ''), 
    services.get("Accompagnement", ''), 
    services.get("Horaires", ''), 
    services.get("Accessibilité", ''), 
    ]
    print(row)
    df.loc[len(df)] = row


if __name__ == '__main__':

    df = pd.DataFrame(
                columns=['id', 'nom',  'adresse', 'code_postal', 'ville', 'derniere_modification', 'email', 'numero',
                'RechercheEmploi', 'DeclarationsEnLigne', 'PremiersPasSurInternet', 'OutilsBureautiques', 'ApprofondissementNumerique',
                'ParentaliteNumerique', 'UsagesProfessionnels', 'OutilsCreatifs', 'Label', 'Accompagnement', 'Horaires', 'Accessibilite' ])

    # on rentre les identifiants de connexion
    print('connected')
    address_parser = parser.AddressParser()

    for i in tqdm(range(3, 560, 1)):
            change_page(f'{CURRENT_URL}{i}')
            sleep(1)
            scrap_assos(i, df, address_parser)

    
    df.to_csv('extract/extrat_Franciline.csv',sep=';', encoding='utf-8-sig', header=True)