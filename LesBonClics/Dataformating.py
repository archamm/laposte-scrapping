import json
from AdresseParser import AdresseParser
from tqdm import tqdm
import pandas as pd
with open("LesBonClics/extrat_lesbonsclics.json", "r") as f:
        data = json.load(f)


full_result = {

    'Bénéficiaires du RSA': 'Non',
    'Travailleurs et indépendants': 'Non',
    'Jeunes': 'Non',
    'Seniors': 'Non',
    'Migrants':'Non',
    "Demandeurs d'emplois": 'Non',
    'Grande précarité': 'Non',
    'Situation de handicap': 'Non',
    'Tout public': 'Non',
    'Ateliers ponctuels': 'Non',
    'Parcours de formation': 'Non',
    'Accompagnement individuel': 'Non',
    'Assistance des usagers sur les services en ligne': 'Non',
    'Accès-libre à un espace équipé ou connecté': 'Non',
    'Diagnostic des compétences numériques': 'Non',
    'Orientation des publics': 'Non',
    'Vente solidaire, prêt ou don de matériel': 'Non',
    'Formation aux bases du numérique': 'Non',
    'Accès aux droits': 'Non',
    'Lien social et communication': 'Non',
    'Santé, accès aux soins': 'Non',
    'Logement': 'Non',
    'Parentalité': 'Non',
    'Mobilité / se déplacer': 'Non',
    'Aide à la consommation': 'Non',
    'Citoyenneté numérique': 'Non',
    'Médiation culturelle': 'Non',
    'Insertion professionnelle': 'Non',
    'Accompagnement budgétaire': 'Non',
    'Loisirs, divertissement, usages ludiques': 'Non',
    'Débutant': 'Non',
    'Intermédiaire': 'Non',
    'Avancé': 'Non',
    'Confirmé': 'Non',
    'Ordinateur': 'Non', 
    'Tablette': 'Non',
    'Smartphone': 'Non',
    'Aucun': 'Non',
    }

df = pd.DataFrame(
        columns=['id', 'nom',  'adresse', 'code_postal', 'ville', 'derniere_modification', 'email', 'site_web', 'numero'])
adr_parser = AdresseParser()
errors = 0
for i in tqdm(range(len(data))):
    element = data[i]
    try:
        result = adr_parser.parse(element['Adresse'])
        ville = result['ville']['nom']
        code_postal = result['code_postal']
    except Exception:
        code_postal = ''
        ville = ''
        errors += 1

    for item in element["Public(s) ciblé(s)"] + element["Equipements d'accompagnement"] + element['Niveau du public'] + element["Thématiques d'accompagnement"] + element['Service(s) proposé(s)']:
            full_result[item] = 'Oui'

    row = [element['id'], element["nom"], element['Adresse'], code_postal, ville, element['Dernière modification'], element['Email'],
     element["Site Web"], element['Numéro']]
    df.loc[len(df)] = row
print(f'errors in postal codes: {errors}')

df.to_csv('extrat_lesbonsclics_GEO.csv',encoding='utf-8-sig', index=False, header=True)