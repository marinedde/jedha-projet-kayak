import boto3
import os

# Nom de ton bucket
BUCKET_NAME = "kayak-project-marine"

# Les fichiers à uploader
files_to_upload = [
    "data/cities_gps.csv",
    "data/weather_raw.csv",
    "data/weather_score.csv",
    "data/hotels_raw.csv",
    "data/hotels_clean.csv"
]

# Connexion à S3
s3 = boto3.client("s3", region_name="eu-west-3")

for filepath in files_to_upload:
    filename = os.path.basename(filepath)  # ex: "cities_gps.csv"
    print(f" Upload de {filename}...")
    
    try:
        s3.upload_file(
            filepath,           # fichier local
            BUCKET_NAME,        # nom du bucket
            f"raw/{filename}"   # chemin dans S3
        )
        print(f"{filename} uploadé dans s3://{BUCKET_NAME}/raw/")
    except Exception as e:
        print(f"Erreur : {e}")

print("\n Tous les fichiers sont dans le Data Lake S3 !")