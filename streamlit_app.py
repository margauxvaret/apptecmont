import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Indian Food EDA",
    page_icon="🍛",
    layout="wide"
)

# Charger les données
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/v61093/Indian-Food-Analysis/main/indian_food.csv'
    return pd.read_csv(url)

# Charger les données
data = load_data()

# Barre latérale pour la navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Menu", ["Accueil", "EDA", "Graphiques Interactifs", "Insights"])

# Titre principal
st.markdown(
    """
    <h1 style="text-align: center; color: #3a5b8a; font-family: Arial, sans-serif;">
        Explorez la Cuisine Indienne 🍛
    </h1>
    """,
    unsafe_allow_html=True
)

# Page : Accueil
if menu == "Accueil":
    st.subheader("Bienvenue !")
    st.write("Cette application vous permet d'explorer un ensemble de données sur la cuisine indienne.")
    st.write("Naviguez dans les sections pour explorer les données et découvrir des insights !")

# Page : EDA (Exploration des données)
elif menu == "EDA":
    st.subheader("Exploration des données (EDA)")
    st.write("Aperçu des données :")
    st.write(data.head())

    # Graphique interactif : Nombre de plats par région
    st.subheader("Nombre de plats par région")
    region_counts = data['region'].value_counts()
    fig = px.bar(
        x=region_counts.index, 
        y=region_counts.values, 
        labels={'x': 'Région', 'y': 'Nombre de plats'},
        title="Répartition des plats par région"
    )
    st.plotly_chart(fig, use_container_width=True)

# Page : Graphiques Interactifs
elif menu == "Graphiques Interactifs":
    st.subheader("Analyse interactive")

    # Filtrer par profil de saveur
    flavor_profile = st.sidebar.selectbox("Sélectionnez un profil de saveur :", ["Tous"] + data['flavor_profile'].dropna().unique().tolist())
    filtered_data = data if flavor_profile == "Tous" else data[data['flavor_profile'] == flavor_profile]

    # Filtrer par temps de préparation
    prep_time_range = st.sidebar.slider(
        "Filtrer par temps de préparation (minutes)",
        min_value=int(data['prep_time'].min()),
        max_value=int(data['prep_time'].max()),
        value=(int(data['prep_time'].min()), int(data['prep_time'].max()))
    )
    filtered_data = filtered_data[
        (filtered_data['prep_time'] >= prep_time_range[0]) & 
        (filtered_data['prep_time'] <= prep_time_range[1])
    ]

    # Graphique interactif : Répartition des temps de préparation
    st.subheader("Répartition des temps de préparation")
    fig = px.histogram(
        filtered_data, 
        x="prep_time", 
        nbins=20, 
        title="Distribution des temps de préparation",
        labels={"prep_time": "Temps de préparation (minutes)"}
    )
    st.plotly_chart(fig, use_container_width=True)

# Page : Insights
elif menu == "Insights":
    st.subheader("Insights")
    avg_prep_time = data.groupby("diet")["prep_time"].mean()
    fig = px.bar(
        avg_prep_time, 
        x=avg_prep_time.index, 
        y=avg_prep_time.values, 
        title="Temps moyen de préparation par type de régime",
        labels={"x": "Type de régime", "y": "Temps moyen de préparation (minutes)"}
    )
    st.plotly_chart(fig, use_container_width=True)
