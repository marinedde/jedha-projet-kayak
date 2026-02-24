# ✈️ Projet Kayak — Pipeline de données voyages

**Jedha Bootcamp · Certification CDSD · Bloc 1**

## 📋 Contexte

Kayak.com, moteur de recherche de voyages filiale de Booking Holdings,
souhaite recommander les meilleures destinations et hôtels à ses utilisateurs
en fonction de la météo réelle. 70% des utilisateurs veulent plus d'infos
sur leur destination avant de réserver.

## 🎯 Objectifs

Construire un pipeline de données complet de bout en bout :
collecte des données météo et hôtels → stockage → transformation → analyse.

## 🏗️ Architecture du Pipeline
```
APIs + Scraping → AWS S3 (Data Lake) → ETL Python → AWS RDS MySQL → Visualisation
```

| Étape | Outil | Description |
|-------|-------|-------------|
| Collecte | APIs + Scraping | Données météo et hôtels |
| Data Lake | AWS S3 | Stockage brut (5 fichiers) |
| ETL | Pandas + Python | Nettoyage et transformation |
| Data Warehouse | AWS RDS MySQL | 3 tables SQL structurées |
| Visualisation | Plotly Maps | Cartes des destinations |

## 🔑 Résultats Clés

- **35 villes** analysées
- **2 509 hôtels** collectés
- **3 tables SQL** créées dans RDS
- **5 fichiers** stockés sur S3

## 🛠️ Stack Technique

- **Python** (requests, pandas, boto3)
- **AWS S3** — Data Lake
- **AWS RDS MySQL** — Data Warehouse
- **Plotly** — visualisations cartographiques
- **VS Code / Jupyter Notebook**

## 📁 Contenu du repo

| Fichier | Description |
|---------|-------------|
| `step1_gps.py, step2_weather.py, step3_scraping.py, step3b_clean_hotels.py, step4_s3_upload.py, step5_etl_rds.py, step6_visualisation.py` | Pipeline complet — collecte, ETL, analyse |
| `Projet_Kayak_CDSD_Bloc1.pptx` | Présentation 7 slides |

---
*Projet réalisé dans le cadre de la certification CDSD Jedha Bootcamp*
