import re
import json
import csv
from bs4 import BeautifulSoup
import datetime

current_date = datetime.datetime.now().strftime('%Y%m%d')

# Définir le chemin du fichier HTML
file_path = 'ObjectifCode/20230924.html'

# Lire le contenu HTML
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Créer un objet BeautifulSoup et spécifier le parseur
soup = BeautifulSoup(content, 'html.parser')

# Trouver tous les éléments de script dans le contenu HTML
scripts = soup.find_all('script')

# Extraire le contenu du script identifié
script_content = str(scripts[2])

# Utiliser une expression régulière pour extraire les objets JavaScript
pattern = re.compile(r'obj\s*=\s*\{(.*?)\};', re.DOTALL)
matches = pattern.findall(script_content)

# Fonction pour convertir une chaîne d'objet JavaScript en une chaîne JSON valide
def js_object_to_json(js_str):
    # Ajouter des guillemets doubles autour des clés
    json_str = re.sub(r'(?<={|,)\s*([a-zA-Z0-9_]+)\s*:', r'"\1":', js_str)
    # Remplacer les valeurs booléennes JavaScript par des valeurs booléennes JSON
    json_str = json_str.replace('True', 'true').replace('False', 'false')
    # Remplacer les guillemets simples par des guillemets doubles
    json_str = json_str.replace("'", '"')
    return json_str

# Initialiser une liste pour contenir les données extraites
data = []

# Parcourir les correspondances et convertir chaque objet JavaScript en dictionnaire Python en utilisant json.loads()
for match in matches:
    # Convertir la chaîne d'objet JavaScript en une chaîne JSON valide
    json_str = js_object_to_json('{' + match + '}')
    # Essayer de charger la chaîne JSON dans un dictionnaire Python
    try:
        obj = json.loads(json_str)
        # Ajouter le dictionnaire à la liste des données extraites
        data.append(obj)
    except json.JSONDecodeError as e:
        print(f"Failed to parse object: {e}")

# Définir le chemin du fichier CSV
csv_file_path = 'ObjectifCode/extracts/ObjectifCode012023_{current_date}.csv'


# Définir l'en-tête du fichier CSV
header = ['address', 'address2', 'capacity', 'capacityReducedMobility', 'city', 'code', 'department',
          'lastMinuteSubscription', 'latitude', 'linkAction', 'linkCenter', 'longitude', 'name', 'phoneNumber',
          'postalCode', 'visualImage']

# Écrire les données extraites dans le fichier CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=header)
    # Écrire l'en-tête dans le fichier CSV
    writer.writeheader()
    # Écrire les lignes dans le fichier CSV
    writer.writerows(data)
