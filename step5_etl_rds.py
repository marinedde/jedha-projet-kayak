import boto3
import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine, text
import io

# ============================================================
# CONFIGURATION
# ============================================================
BUCKET_NAME = "kayak-project-marine"

# À remplacer par ton endpoint RDS quand l'instance est disponible
RDS_HOST = "kayak-db.c9eaa6c44d7i.eu-west-3.rds.amazonaws.com"
RDS_PORT = 3306
RDS_USER = "admin"
RDS_PASSWORD = "Lagon23?"
RDS_DB = "kayak"

# ============================================================
# ÉTAPE 1 : Lire les données depuis S3
# ============================================================
print(" Lecture des données depuis S3...")

s3 = boto3.client("s3", region_name="eu-west-3")

def read_csv_from_s3(filename):
    """Lit un CSV depuis S3 et le retourne en DataFrame."""
    response = s3.get_object(Bucket=BUCKET_NAME, Key=f"raw/{filename}")
    content = response["Body"].read().decode("utf-8")
    return pd.read_csv(io.StringIO(content))

df_cities = read_csv_from_s3("cities_gps.csv")
df_weather = read_csv_from_s3("weather_score.csv")
df_hotels = read_csv_from_s3("hotels_clean.csv")

print(f" Villes : {len(df_cities)} lignes")
print(f" Météo : {len(df_weather)} lignes")
print(f" Hôtels : {len(df_hotels)} lignes")

# ============================================================
# ÉTAPE 2 : Transformer les données
# ============================================================
print("\n Transformation des données...")

# Nettoyer les noms de colonnes (pas d'espaces, tout en minuscules)
df_cities.columns = df_cities.columns.str.lower().str.replace(" ", "_")
df_weather.columns = df_weather.columns.str.lower().str.replace(" ", "_")
df_hotels.columns = df_hotels.columns.str.lower().str.replace(" ", "_")

# Arrondir les valeurs numériques météo
df_weather["avg_temp"] = df_weather["avg_temp"].round(2)
df_weather["avg_temp_max"] = df_weather["avg_temp_max"].round(2)
df_weather["total_rain"] = df_weather["total_rain"].round(2)
df_weather["avg_humidity"] = df_weather["avg_humidity"].round(2)
df_weather["weather_score"] = df_weather["weather_score"].round(2)

# Arrondir les coordonnées GPS hôtels
df_hotels["latitude"] = df_hotels["latitude"].round(6)
df_hotels["longitude"] = df_hotels["longitude"].round(6)

print(" Transformation terminée")

# ============================================================
# ÉTAPE 3 : Charger dans RDS
# ============================================================
print("\n Connexion à RDS...")

engine = create_engine(
    f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/"
)

# Créer la base de données
with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {RDS_DB}"))
    conn.execute(text(f"USE {RDS_DB}"))
    print(f" Base de données '{RDS_DB}' créée")

# Reconnexion avec la base
engine = create_engine(
    f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DB}"
)

# Chargement des tables
print("\n Chargement des tables...")

df_cities.to_sql("cities", engine, if_exists="replace", index=False)
print(f" Table 'cities' : {len(df_cities)} lignes")

df_weather.to_sql("weather", engine, if_exists="replace", index=False)
print(f" Table 'weather' : {len(df_weather)} lignes")

df_hotels.to_sql("hotels", engine, if_exists="replace", index=False)
print(f" Table 'hotels' : {len(df_hotels)} lignes")

print("\n ETL terminé ! Les données sont dans RDS.")

# ============================================================
# VÉRIFICATION : Quelques requêtes SQL
# ============================================================
print("\n Vérification avec quelques requêtes SQL...")

with engine.connect() as conn:
    # Top 5 destinations météo
    result = conn.execute(text("""
        SELECT c.city, w.avg_temp, w.total_rain, w.weather_score
        FROM weather w
        JOIN cities c ON w.city_id = c.id
        ORDER BY w.weather_score DESC
        LIMIT 5
    """))
    print("\n Top 5 destinations météo :")
    for row in result:
        print(f"   {row[0]} → score: {row[3]}, temp: {row[1]}°C, pluie: {row[2]}mm")

    # Nombre d'hôtels par ville
    result = conn.execute(text("""
        SELECT city, COUNT(*) as nb_hotels
        FROM hotels
        GROUP BY city
        ORDER BY nb_hotels DESC
        LIMIT 5
    """))
    print("\n Top 5 villes par nombre d'hôtels :")
    for row in result:
        print(f"   {row[0]} → {row[1]} hôtels")