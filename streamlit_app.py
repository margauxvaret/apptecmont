import streamlit as st
import pandas as pd
import plotly.express as px

# Configuration de la page
st.set_page_config(
    page_title="Indian Food EDA",
    page_icon="🍛",
    layout="centered"
)

st.markdown("""
    <style>
        /* Background color for main page */
        .main {
            background-color: #e8f0fe;
        }

        /* Custom styles for header and text colors */
        h1, h2, h3 {
            color: #3a5b8a;
            font-family: Arial, sans-serif;
        }

        /* Styles for top menu */
        .stSelectbox {
            color: white;
            background-color: #3a5b8a;
            padding: 5px;
            border-radius: 5px;
        }

        /* Button styles */
        .stButton>button {
            background-color: #3a5b8a;
            color: white;
            border-radius: 5px;
        }
        .stButton>button:hover {
            background-color: #2b3f73;
            color: #f0f2f6;
        }
    </style>
""", unsafe_allow_html=True)


# URL de la Google Sheet
gsheetid = '1i0PYy2SjPivU0xDRC2DY8kaAduSJRBNVCgakzfCwdr0'
sheetid='113565780'
url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv'

# Fonction pour charger les données depuis Google Sheets
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

# Chargement des données
data = load_data(url)
st.title("Indian Food")
st.write("Aperçu des données :")
st.write(data.head())

# Création des colonnes pour les graphiques
col1, col2 = st.columns(2)

# Menu de navigation
menu = st.selectbox(
    "Navigation",
    ["Home", "EDA", "Insights", "Prediction"],
    key="main_menu"
)


# Page d'accueil
if menu == "Home":
    st.title("Indian Food")
    st.write("Look at the pretty waves")
    st.write("Cette application vous permet d'explorer un ensemble de données sur la cuisine indienne.")
    st.write(data.head())

# Page EDA (Exploration des données)
elif menu == "EDA":
    st.title("Exploration des données (EDA)")

    # Graphique 1 : Nombre de plats par région
    st.subheader("Nombre de plats par région")
    region_counts = data['region'].value_counts()
    fig1 = px.bar(region_counts, x=region_counts.index, y=region_counts.values, labels={'x': 'Région', 'y': 'Nombre de plats'})
    st.plotly_chart(fig1, use_container_width=True)

    # Graphique 2 : Distribution des types de régimes
    st.subheader("Distribution des types de régimes")
    diet_counts = data['diet'].value_counts()
    fig2 = px.pie(values=diet_counts.values, names=diet_counts.index, title="Répartition des types de régimes")
    st.plotly_chart(fig2, use_container_width=True)

# Page Insights
elif menu == "Insights":
    st.title("Insights")

    # Graphique : Temps moyen de préparation par type de régime
    st.subheader("Temps moyen de préparation par type de régime")
    avg_prep_time_by_diet = data.groupby("diet")["prep_time"].mean().dropna()
    fig3 = px.bar(avg_prep_time_by_diet, x=avg_prep_time_by_diet.index, y=avg_prep_time_by_diet.values, labels={'x': 'Type de régime', 'y': 'Temps moyen de préparation (minutes)'})
    st.plotly_chart(fig3, use_container_width=True)


# Page Prediction (Prédiction)
elif menu == "Prediction":
    st.title("Prediction")
    st.write("Actuellement, aucune prédiction n'est implémentée.")
    st.write("")

# Rafraîchissement des données
if st.button("Rafraîchir les données"):
    data = load_data()
    st.write("Données rafraîchies!")
    st.write(data.head())
