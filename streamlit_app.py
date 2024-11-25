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
    fig_pie_flavor = px.pie(
        names=flavor_counts.index, 
        values=flavor_counts.values,
        title="Répartition des profils de saveurs",
        labels={'label': 'Profil de saveur'}
    )
    st.plotly_chart(fig_pie_flavor, use_container_width=True)

# Page : Graphiques Interactifs
elif menu == "Graphiques Interactifs":
    st.subheader("Analyse interactive")

    # Nuage de points : Temps de préparation vs Temps de cuisson
    st.subheader("Temps de préparation vs Temps de cuisson")
    fig_scatter = px.scatter(
        data,
        x="prep_time",
        y="cook_time",
        color="diet",
        size="cook_time",
        hover_data=["name"],
        title="Relation entre le temps de préparation et de cuisson",
        labels={"prep_time": "Temps de préparation (minutes)", "cook_time": "Temps de cuisson (minutes)"}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # Graphique circulaire : Répartition des régimes
    st.subheader("Répartition des régimes")
    diet_counts = data['diet'].value_counts()
    fig_pie_diet = px.pie(
        names=diet_counts.index, 
        values=diet_counts.values,
        title="Répartition des régimes (Végétarien vs Non Végétarien)"
    )
    st.plotly_chart(fig_pie_diet, use_container_width=True)

# Page : Insights
elif menu == "Insights":
    st.subheader("Insights")

    # Graphique en ligne : Évolution du temps de préparation (cumulatif)
    st.subheader("Évolution cumulative du temps de préparation par type de régime")
    cumulative_prep_time = data.groupby("diet")["prep_time"].cumsum()
    data["cumulative_prep_time"] = cumulative_prep_time
    fig_line = px.line(
        data,
        x=data.index,
        y="cumulative_prep_time",
        color="diet",
        title="Temps de préparation cumulatif",
        labels={"cumulative_prep_time": "Temps cumulatif (minutes)"}
    )
    st.plotly_chart(fig_line, use_container_width=True)

# Page : Analyse Régionale
elif menu == "Analyse Régionale":
    st.subheader("Analyse régionale des plats")

    # Graphique à bulles : Nombre de plats par région et type de régime
    st.subheader("Analyse des plats par région et type de régime")
    bubble_data = data.groupby(['region', 'diet']).size().reset_index(name='count')
    fig_bubble = px.scatter(
        bubble_data,
        x="region",
        y="diet",
        size="count",
        color="region",
        title="Nombre de plats par région et régime",
        labels={"count": "Nombre de plats", "region": "Région", "diet": "Type de régime"}
    )
    st.plotly_chart(fig_bubble, use_container_width=True)
