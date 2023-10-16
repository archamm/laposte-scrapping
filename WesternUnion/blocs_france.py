import csv
from geopy.distance import geodesic

# Les coordonnées approximatives de la France
lat_min, lat_max = 41.303, 51.124
lon_min, lon_max = -5.266, 9.662

# La taille de chaque carré en km
square_size = 50

# Convertir en degrés (approximatif, varie selon la latitude)
square_size_deg = square_size / 111

# Préparez le fichier CSV
with open('france_coordinates.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Latitude", "Longitude"]) # Écrire les en-têtes

    # Générez les coordonnées et écrivez-les dans le fichier CSV
    lat = lat_min
    while lat < lat_max:
        lon = lon_min
        while lon < lon_max:
            writer.writerow([lat, lon])
            lon += square_size_deg
        lat += square_size_deg