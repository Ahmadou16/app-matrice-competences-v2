import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Titre de l'application
st.title("🔍 Matrice de Compétences - Version Simplifiée")

# Charger le fichier Excel
uploaded_file = st.file_uploader("📁 Charger le fichier Excel de la matrice de compétences", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, engine="openpyxl")

        # Suppression des colonnes totalement vides
        df.dropna(how="all", axis=1, inplace=True)

        # Sélection des colonnes de compétences uniquement (hors colonnes d'identité si nécessaire)
        colonnes_utiles = df.columns[1:]  # on suppose que la première colonne est le nom du consultant

        # Choix d'une compétence à filtrer
        selected_comp = st.selectbox("🧠 Choisissez une compétence :", colonnes_utiles)

        # Niveau minimum requis
        niveau_min = st.slider("🎯 Niveau minimum requis :", 0, 4, 2)

        # Appliquer le filtre
        try:
            filtres = df[df[selected_comp] >= niveau_min]

            # Affichage du tableau filtré
            st.subheader(f"📋 Consultants ayant '{selected_comp}' à un niveau ≥ {niveau_min}")
            st.dataframe(filtres)

            # ➕ Graphique des niveaux
            st.subheader("📊 Répartition des niveaux pour la compétence sélectionnée")
            niveau_counts = df[selected_comp].value_counts().sort_index()

            fig, ax = plt.subplots()
            bars = ax.bar(niveau_counts.index.astype(str), niveau_counts.values, color='#4C72B0')

            ax.set_xlabel("Niveau")
            ax.set_ylabel("Nombre de consultants")
            ax.set_title(f"Répartition des niveaux pour '{selected_comp}'")

            for bar in bars:
                yval = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, yval + 0.1, int(yval), ha='center', va='bottom')

            st.pyplot(fig)

            # ➕ Télécharger le tableau filtré
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtres.to_excel(writer, index=False)
            output.seek(0)

            st.download_button(
                label="📥 Télécharger le fichier filtré",
                data=output,
                file_name="consultants_filtres.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        except Exception as e:
            st.error(f"Erreur pendant le filtrage : {e}")

    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du fichier : {e}")
