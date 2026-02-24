import pandas as pd

df = pd.read_csv("data/hotels_raw.csv")
print(f"Hôtels bruts : {len(df)}")

# 1. On garde uniquement les hôtels avec coordonnées GPS
df = df.dropna(subset=["latitude", "longitude"])
print(f"Après suppression sans GPS : {len(df)}")

# 2. Convertir le score en nombre (ex: "4.5" → 4.5)
df["score"] = pd.to_numeric(df["score"], errors="coerce")

# 3. Remplir les valeurs manquantes restantes
df["description"] = df["description"].fillna("Non renseigné")
df["score"] = df["score"].fillna(df["score"].median())

# 4. Supprimer les doublons sur le nom + ville
df = df.drop_duplicates(subset=["hotel_name", "city"])
print(f"Après suppression doublons : {len(df)}")

# 5. Ajouter un identifiant unique
df = df.reset_index(drop=True)
df["hotel_id"] = df.index + 1

# 6. Réorganiser les colonnes
df = df[["hotel_id", "city_id", "city", "hotel_name", 
         "score", "description", "url", 
         "latitude", "longitude"]]

print(f"\n Dataset final : {len(df)} hôtels")
print(df.head())

# Sauvegarde
df.to_csv("data/hotels_clean.csv", index=False)
print("\n Fichier hotels_clean.csv sauvegardé !")