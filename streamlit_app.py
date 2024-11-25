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
menu = st.sidebar.radio("Menu", ["Accueil", "EDA", "Graphiques Interactifs", "Insights", "Analyse Régionale"])

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

    # Graphique circulaire : Distribution des profils de saveurs
    st.subheader("Distribution des profils de saveurs")
    flavor_counts = data['flavor_profile'].value_counts()
    st.write(f"Profils de saveurs disponibles : {', '.join(data['flavor_profile'].dropna().unique())}")
    fig_pie_flavor = px.pie(
        names=flavor_counts.index, 
        values=flavor_counts.values,
        title="Répartition des profils de saveurs",
        labels={'label': 'Profil de saveur'}
    )
    st.plotly_chart(fig_pie_flavor, use_container_width=True)

# Page : Graphiques Interactifs
elif menu == "Graphiques Interactifs":
    st.subheader("Graphiques interactifs")

    # Graphique en barres : Nombre de plats par région
    st.subheader("Nombre de plats par région")
    region_counts = data['region'].value_counts()
    fig_bar_region = px.bar(
        x=region_counts.index, 
        y=region_counts.values,
        labels={'x': 'Région', 'y': 'Nombre de plats'},
        title="Nombre de plats par région"
    )
    st.plotly_chart(fig_bar_region, use_container_width=True)

    # Graphique en barres : Distribution des types de régimes
    st.subheader("Distribution des types de régimes")
    diet_counts = data['diet'].value_counts()
    fig_bar_diet = px.bar(
        x=diet_counts.index,
        y=diet_counts.values,
        labels={'x': 'Type de régime', 'y': 'Nombre de plats'},
        title="Distribution des types de régimes"
    )
    st.plotly_chart(fig_bar_diet, use_container_width=True)

# Page : Insights
elif menu == "Insights":
    st.subheader("Insights")

    # Graphique en ligne : Évolution cumulative du temps de préparation par index
    st.subheader("Temps de préparation cumulatif")
    data_sorted = data.sort_values(by="prep_time", ascending=True)
    data_sorted['prep_time_cumsum'] = data_sorted['prep_time'].cumsum()
    st.line_chart(data_sorted['prep_time_cumsum'])

# Page : Analyse Régionale
elif menu == "Analyse Régionale":
    st.subheader("Analyse régionale des plats")

    # Graphique circulaire : Nombre de plats par région
    st.subheader("Répartition des plats par région")
    region_counts = data['region'].value_counts()
    fig_pie_region = px.pie(
        names=region_counts.index,
        values=region_counts.values,
        title="Proportion des plats par région"
    )
    st.plotly_chart(fig_pie_region, use_container_width=True)
