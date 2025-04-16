import streamlit as st
import pandas as pd

# Chargement du fichier Excel
fichier = st.file_uploader("Importer le fichier Excel de la matrice de compétences", type=["xlsx"])

if fichier:
    df = pd.read_excel(fichier, sheet_name=0)

    # On récupère les colonnes à partir de la 2ème (index 1), car la 1ère contient les noms
    competences = df.columns[1:]

    # Création d’un dictionnaire Catégorie → [Sous-compétences]
    categories = {}
    for comp in competences:
        if isinstance(comp, tuple):
            categorie, sous_competence = comp
        else:
            # Si le nom de la compétence a été mis à plat, on tente de l'extraire manuellement
            try:
                categorie, sous_competence = comp.split(" - ", 1)
            except ValueError:
                categorie, sous_competence = "Autres", comp
        categories.setdefault(categorie.strip(), []).append(comp)

    st.header("Filtrer les consultants par compétence")

    # Étape 1 : sélection de la catégorie
    selected_cat = st.selectbox("Choisir une catégorie", list(categories.keys()))

    # Étape 2 : sélection de la sous-compétence
    selected_comp = st.selectbox("Choisir une compétence", categories[selected_cat])

    # Choix du niveau minimum
    niveau_min = st.slider("Niveau minimum requis (0 à 4)", min_value=0, max_value=4, value=2)

    # Vérification et filtrage
    if selected_comp in df.columns:
        try:
            df[selected_comp] = pd.to_numeric(df[selected_comp], errors='coerce')  # Assure que ce soit bien des nombres
            filtres = df[df[selected_comp] >= niveau_min]
            st.success(f"{len(filtres)} consultant(s) trouvé(s) avec un niveau ≥ {niveau_min} en '{selected_comp}'")
            st.dataframe(filtres)

            # Option de téléchargement
            st.download_button(
                label="Télécharger le fichier filtré",
                data=filtres.to_excel(index=False, engine="openpyxl"),
                file_name="consultants_filtres.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"Erreur pendant le filtrage : {e}")
    else:
        st.warning("Compétence non trouvée dans le fichier.")
