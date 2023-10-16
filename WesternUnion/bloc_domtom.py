import csv

# Définir les limites approximatives de latitude et longitude pour chaque DOM-TOM
regions = {
    'Guadeloupe': {'lat_min': 15.8, 'lat_max': 16.5, 'lon_min': -61.9, 'lon_max': -61.0},
    'Martinique': {'lat_min': 14.3, 'lat_max': 14.9, 'lon_min': -61.3, 'lon_max': -60.7},
    'Guyane': {'lat_min': 2.1, 'lat_max': 5.8, 'lon_min': -54.6, 'lon_max': -51.6},
    'Reunion': {'lat_min': -21.4, 'lat_max': -20.8, 'lon_min': 55.2, 'lon_max': 55.9},
    'Mayotte': {'lat_min': -13.0, 'lat_max': -12.6, 'lon_min': 45.0, 'lon_max': 45.3}
}

# La taille de chaque carré en km
square_size = 50

# Convertir en degrés (approximatif, varie selon la latitude)
square_size_deg = square_size / 111

# Préparez le fichier CSV
with open('dom_tom_coordinates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Region", "Latitude", "Longitude"])  # Écrire les en-têtes

    # Générer les coordonnées pour chaque DOM-TOM
    for region, coords in regions.items():
        lat_min, lat_max = coords['lat_min'], coords['lat_max']
        lon_min, lon_max = coords['lon_min'], coords['lon_max']

        lat = lat_min
        while lat < lat_max:
            lon = lon_min
            while lon < lon_max:
                writer.writerow([region, lat, lon])
                lon += square_size_deg
            lat += square_size_deg
