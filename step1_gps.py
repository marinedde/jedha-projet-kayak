import requests
import pandas as pd
import time

# Liste des 35 villes
cities = [
    "Mont Saint Michel", "St Malo", "Bayeux", "Le Havre", "Rouen",
    "Paris", "Amiens", "Lille", "Strasbourg", "Chateau du Haut Koenigsbourg",
    "Colmar", "Eguisheim", "Besancon", "Dijon", "Annecy", "Grenoble",
    "Lyon", "Gorges du Verdon", "Bormes les Mimosas", "Cassis",
    "Marseille", "Aix en Provence", "Avignon", "Uzes", "Nimes",
    "Aigues Mortes", "Saintes Maries de la mer", "Collioure", "Carcassonne",
    "Ariege", "Toulouse", "Montauban", "Biarritz", "Bayonne", "La Rochelle"
]

def get_gps(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city_name + ", France",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "kayak-project/1.0"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        return None, None

# Boucle sur toutes les villes
results = []
for i, city in enumerate(cities):
    lat, lon = get_gps(city)
    results.append({
        "id": i + 1,
        "city": city,
        "latitude": lat,
        "longitude": lon
    })
    print(f" {city} → lat={lat}, lon={lon}")
    time.sleep(1)

# Création du DataFrame et sauvegarde
df_cities = pd.DataFrame(results)
df_cities.to_csv("data/cities_gps.csv", index=False)
print("\n Fichier cities_gps.csv sauvegardé dans data/")