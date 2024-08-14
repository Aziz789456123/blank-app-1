import pandas as pd
import streamlit as st
import plotly.express as px
import json
from pandas.api.types import is_string_dtype

st.title("Analyse des risques pour assurance")

# Téléchargement des fichiers
uploaded_files = {
    'inscription': st.file_uploader("Télécharger le fichier des inscriptions", type="xlsx"),
    'foyer': st.file_uploader("Télécharger le fichier des foyers", type="xlsx"),
    'individu': st.file_uploader("Télécharger le fichier des individus", type="xlsx"),
    'accident': st.file_uploader("Télécharger le fichier des accidents", type="xlsx")
}

# Vérification que tous les fichiers sont téléchargés
if all(uploaded_files.values()):
    # Chargement des données
    @st.cache_data
    def load_data(uploaded_files):
        dfs = {}
        for key, file in uploaded_files.items():
            dfs[key] = pd.read_excel(file)
            # Traiter les colonnes JSON si besoin
            for col in dfs[key].columns:
                if is_string_dtype(dfs[key][col]):
                    try:
                        dfs[key][col] = dfs[key][col].apply(lambda x: json.dumps(x) if isinstance(x, dict) else x)
                    except (json.JSONDecodeError, TypeError):
                        pass  # Ignorer si la colonne n'est pas JSON
        return dfs

    dfs = load_data(uploaded_files)
