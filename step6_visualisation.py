import pandas as pd
import plotly.express as px

# Chargement des données
df_weather = pd.read_csv("data/weather_score.csv")
df_hotels = pd.read_csv("data/hotels_clean.csv")
df_cities = pd.read_csv("data/cities_gps.csv")

# Jointure météo + coordonnées GPS
df_map = df_weather.merge(df_cities[["id", "latitude", "longitude"]], 
                           left_on="city_id", right_on="id")

# ============================================================
# CARTE 1 : Top 5 destinations météo
# ============================================================
df_top5 = df_map.sort_values("weather_score", ascending=False).head(5)

fig1 = px.scatter_map(
    df_top5,
    lat="latitude",
    lon="longitude",
    size="weather_score",
    color="avg_temp",
    hover_name="city",
    hover_data={
        "avg_temp": ":.1f",
        "total_rain": ":.1f",
        "weather_score": ":.2f"
    },
    color_continuous_scale="RdYlGn",
    size_max=40,
    zoom=4,
    center={"lat": 46.5, "lon": 2.5},
    map_style="carto-positron",
    title=" Top 5 destinations météo en France"
)

fig1.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig1.write_html("data/map_top5_destinations.html")
print(" Carte 1 sauvegardée : map_top5_destinations.html")

# ============================================================
# CARTE 2 : Top 20 hôtels les plus populaires
# ============================================================

# On garde uniquement les hôtels des top 5 villes
top5_cities = df_top5["city"].tolist()
df_top_hotels = df_hotels[df_hotels["city"].isin(top5_cities)].copy()

# Trier par score et prendre les 20 meilleurs
df_top_hotels = df_top_hotels.dropna(subset=["score"])
df_top_hotels["score"] = pd.to_numeric(df_top_hotels["score"], errors="coerce")
df_top20 = df_top_hotels.sort_values("score", ascending=False).head(20)

fig2 = px.scatter_map(
    df_top20,
    lat="latitude",
    lon="longitude",
    size="score",
    color="score",
    hover_name="hotel_name",
    hover_data={
        "city": True,
        "score": ":.1f",
        "description": True
    },
    color_continuous_scale="Blues",
    size_max=30,
    zoom=4,
    center={"lat": 46.5, "lon": 2.5},
    map_style="carto-positron",
    title="🏨 Top 20 hôtels des meilleures destinations"
)

fig2.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
fig2.write_html("data/map_top20_hotels.html")
print(" Carte 2 sauvegardée : map_top20_hotels.html")

print("\n Visualisations terminées !")
print(f"\n Top 5 destinations : {df_top5['city'].tolist()}")
print(f" Top 20 hôtels dans : {df_top20['city'].unique().tolist()}")