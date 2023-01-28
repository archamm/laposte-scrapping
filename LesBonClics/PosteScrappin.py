import json
import warnings
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from tqdm import tqdm

warnings.filterwarnings("ignore", category=DeprecationWarning)


option = webdriver.ChromeOptions()
option.add_argument("— incognito")
option.add_argument("--window-size=1440,1000")
#option.add_argument('--headless') # permet d'afficher ou non le navigateur et ce qu'effectue commme actions le programme
option.add_argument('--no-sandbox')
CHROME_PATH = r'/usr/local/bin/ls'  # path from 'which chromedriver'

BROWSER = webdriver.Chrome(chrome_options=option)
CURRENT_URL = 'https://www.lesbonsclics.fr/fr/login/'

ID = "isnlaposte@gmail.com"
MDP = "isnlaposte2020"

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



'''clique sur un boutton grace a son xpath'''


def click_button(xpath):
    BROWSER.find_element("xpath", xpath).click()


def connexion():
    wait_for_element_to_appear('/html/body/div[2]/div[2]/form/div[1]/input')
    BROWSER.find_element("xpath",'/html/body/div[2]/div[2]/form/div[1]/input').send_keys \
        (ID)
    BROWSER.find_element("xpath",'/html/body/div[2]/div[2]/form/div[2]/input').send_keys \
        (MDP)
    BROWSER.find_element("xpath",'/html/body/div[2]/div[2]/form/div[3]/button').click()
    # on clique sur le bouton continue ensuite
    # browser.find_element_by_xpath('// *[ @ id = "hlnkContinue"]').click()


def scrap_assos(id,res, df):


    try:
        name = BROWSER.find_element("xpath",'/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/div[1]/label/span').text
    except Exception:
        return
    numero = ''
    website = ''
    email = ''
    last_modification = ''
    adress = ''
    try:
        last_modification = BROWSER.find_element("xpath",'/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/div[2]/label[2]/span').text.replace('le ', '').replace(' Suggérer une modification', '')
    except Exception:
        print(f'{id} has no last mod')
    try:
        email = BROWSER.find_element("xpath",'/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/div[7]/label/span/a').text
    except Exception:
        print(f'{id} has no email')
    try:
        website = BROWSER.find_element("xpath",'/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/div[6]/label/span/a').text
    except Exception:
        print(f'{id} has no website')
    try:
        numero = BROWSER.find_element("xpath",'/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/div[8]/label/span').text
    except Exception:
        print(f'{id} has no phone number')
    try:
        adress = BROWSER.find_element("xpath",'/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/div[3]/label/span').text
    except Exception:
        print(f'{id} has no adress')

    checkboxes = BROWSER.find_elements(By.CLASS_NAME, 'checkbox-component.container-check.smaller')
    targets = []
    services = []
    thematique = []
    targetLevel = []
    equipement = []

    for checkbox in checkboxes:
        elements = checkbox.find_elements('xpath', './/*')
        if elements[0].get_attribute("name") == 'structure_edit[targets][]' and elements[0].is_selected():
            targets.append(elements[2].text)
        elif elements[0].get_attribute("name") == 'structure_edit[services][]' and elements[0].is_selected():
            services.append(elements[2].text)
        elif elements[0].get_attribute("name") == 'structure_edit[thematique][]' and elements[0].is_selected():
            thematique.append(elements[2].text)
        elif elements[0].get_attribute("name") == 'structure_edit[targetLevels][]' and elements[0].is_selected():
            targetLevel.append(elements[2].text)
        elif elements[0].get_attribute("name") == 'structure_edit[equipement][]' and elements[0].is_selected():
            equipement.append(elements[2].text)
    res.append({'id': id, 'nom' : name, 'Adresse' : adress,'Dernière modification' : last_modification, 'Email': email, 'Site Web': website,'Numéro': numero,
     'Public(s) ciblé(s)': targets, 'Service(s) proposé(s)': services,
      "Thématiques d'accompagnement": thematique, 'Niveau du public' : targetLevel, "Equipements d'accompagnement": equipement})
    row = [id, name, adress, last_modification, email, website, numero, targets, services, thematique, targetLevel, equipement]
    df.loc[len(df)] = row


if __name__ == '__main__':

    df = pd.DataFrame(
        columns=['id', 'nom',  'Adresse', 'Dernière modification', 'Email', 'Site Web', 'Numéro', 'Public(s) ciblé(s)', 'Service(s) proposé(s)', "Thématiques d'accompagnement",
        'Niveau du public', "Equipements d'accompagnement"])
    change_page(CURRENT_URL)
    # on rentre les identifiants de connexion
    connexion()
    print('connected')
    res = []
    for i in tqdm(range(5, 8300, 1)):
            change_page(f'https://www.lesbonsclics.fr/fr/espace-pro/structure/voir/{i}')
            scrap_assos(i, res, df)

    print(res)
    with open('extrat_lesbonsclics.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(res, ensure_ascii=False))
    df.to_csv('extrat_lesbonsclics.csv',sep=';', header=True)