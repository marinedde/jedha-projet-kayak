import requests
import pandas as pd
import time

df_cities = pd.read_csv("data/cities_gps.csv")

def get_hotels(city_id, city_name, lat, lon):
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    query = f"""
    [out:json][timeout:25];
    (
      node["tourism"="hotel"](around:10000,{lat},{lon});
      way["tourism"="hotel"](around:10000,{lat},{lon});
    );
    out body;
    """
    
    try:
        response = requests.post(overpass_url, data={"data": query})
        
        # Vérifie que la réponse n'est pas vide
        if not response.text.strip():
            print(f"   ⚠️ Réponse vide pour {city_name}, on réessaie...")
            time.sleep(10)
            response = requests.post(overpass_url, data={"data": query})
        
        data = response.json()
        
    except Exception as e:
        print(f"   ❌ Erreur pour {city_name}: {e}, on passe...")
        return []
    
    hotels = []
    for element in data.get("elements", []):
        tags = element.get("tags", {})
        name = tags.get("name")
        
        if not name:
            continue
            
        if element["type"] == "node":
            h_lat = element.get("lat")
            h_lon = element.get("lon")
        else:
            h_lat = element.get("center", {}).get("lat")
            h_lon = element.get("center", {}).get("lon")
        
        hotels.append({
            "city_id": city_id,
            "city": city_name,
            "hotel_name": name,
            "url": f"https://www.booking.com/search.html?ss={name.replace(' ', '+')}",
            "score": tags.get("stars", None),
            "description": tags.get("addr:full", tags.get("addr:street", None)),
            "phone": tags.get("phone", None),
            "website": tags.get("website", None),
            "latitude": h_lat,
            "longitude": h_lon
        })
    
    return hotels

# Boucle sur toutes les villes
all_hotels = []
for _, row in df_cities.iterrows():
    print(f" Récupération hôtels pour {row['city']}...")
    hotels = get_hotels(row["id"], row["city"], row["latitude"], row["longitude"])
    print(f"   → {len(hotels)} hôtels trouvés")
    all_hotels.extend(hotels)
    time.sleep(5)  # ← on passe de 2 à 5 secondes

# Sauvegarde
df_hotels = pd.DataFrame(all_hotels)
df_hotels.to_csv("data/hotels_raw.csv", index=False)
print(f"\n {len(df_hotels)} hôtels sauvegardés dans data/hotels_raw.csv")
print(df_hotels.head())