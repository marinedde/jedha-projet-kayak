import requests
import pandas as pd
import time

# Ta clé API OpenWeatherMap
API_KEY = "YOUR_API_KEY_HERE"

# On charge le fichier GPS qu'on vient de créer
df_cities = pd.read_csv("data/cities_gps.csv")

def get_weather(city_id, city_name, lat, lon):
    """
    Appelle l'API OpenWeatherMap One Call pour obtenir
    les prévisions sur 7 jours.
    """
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",   # températures en Celsius
        "lang": "fr"
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "list" not in data:
        print(f" Erreur pour {city_name}: {data}")
        return []

    results = []
    for forecast in data["list"]:
        results.append({
            "city_id": city_id,
            "city": city_name,
            "datetime": forecast["dt_txt"],
            "temp": forecast["main"]["temp"],
            "temp_min": forecast["main"]["temp_min"],
            "temp_max": forecast["main"]["temp_max"],
            "humidity": forecast["main"]["humidity"],
            "weather": forecast["weather"][0]["description"],
            "wind_speed": forecast["wind"]["speed"],
            "rain": forecast.get("rain", {}).get("3h", 0)  # pluie en mm (0 si absent)
        })
    return results

# Boucle sur toutes les villes
all_weather = []
for _, row in df_cities.iterrows():
    print(f" Récupération météo pour {row['city']}...")
    weather_data = get_weather(row["id"], row["city"], row["latitude"], row["longitude"])
    all_weather.extend(weather_data)
    time.sleep(1)

# Création du DataFrame
df_weather = pd.DataFrame(all_weather)

# Calcul du score météo par ville sur 7 jours
# On moyenne la température max et on somme la pluie
df_score = df_weather.groupby(["city_id", "city"]).agg(
    avg_temp=("temp", "mean"),
    avg_temp_max=("temp_max", "mean"),
    total_rain=("rain", "sum"),
    avg_humidity=("humidity", "mean"),
    avg_wind=("wind_speed", "mean")
).reset_index()

# Score météo : on favorise chaleur et absence de pluie
df_score["weather_score"] = df_score["avg_temp"] - df_score["total_rain"] - (df_score["avg_humidity"] / 10)

# Tri par meilleur score
df_score = df_score.sort_values("weather_score", ascending=False)

print("\n Top 10 des meilleures destinations météo :")
print(df_score[["city", "avg_temp", "total_rain", "weather_score"]].head(10))

# Sauvegarde
df_weather.to_csv("data/weather_raw.csv", index=False)
df_score.to_csv("data/weather_score.csv", index=False)
print("\n Fichiers weather_raw.csv et weather_score.csv sauvegardés !")
