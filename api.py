from fastapi import FastAPI
import pandas as pd

app = FastAPI(
    title="Indian Food API 🍛",
    description="Une API simple pour explorer les saveurs et régions de la cuisine indienne.",
    version="1.0.0"
)

#chargement des données
url = 'https://raw.githubusercontent.com/v61093/Indian-Food-Analysis/main/indian_food.csv'
data = pd.read_csv(url)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API Indian Food 🍛"}

@app.get("/regions")
def get_regions():
    """Retourne le nombre de plats par région"""
    return data["region"].value_counts().to_dict()

@app.get("/flavors")
def get_flavors():
    """Retourne la répartition des profils de saveurs"""
    return data["flavor_profile"].value_counts().to_dict()

@app.get("/diet")
def get_diet_distribution():
    """Retourne la distribution des régimes (végétarien, non-végétarien, etc.)"""
    return data["diet"].value_counts().to_dict()
