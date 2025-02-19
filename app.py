import streamlit as st
import pandas as pd
import os

# === Configuration du dossier de stockage des PDF ===
# Crée un dossier pour stocker les fichiers PDF s'il n'existe pas
PDF_FOLDER = "pdf_factures"
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# === Initialisation des données ===
# Si tu veux démarrer avec un tableau vide, mets simplement des listes vides []
achats_data = {
    "Date": ["2025-01-10", "2025-01-15", "2025-01-20"],
    "Numéro de Facture": ["FA-001", "FA-002", "FA-003"],
    "Description": ["Engin de chantier A", "Pièces détachées B", "Matériaux C"],
    "Montant TTC": [18000, 600, 2400],
    "Statut": ["Payée", "En attente", "Payée"],
    "Fichier PDF": ["FA-001.pdf", "FA-002.pdf", "FA-003.pdf"]
}

# Convertir en DataFrame
achats_df = pd.DataFrame(achats_data)

# === Titre de l'application ===
st.title("Gestion des Achats et Factures avec PDF Intégré")

# === Formulaire pour ajouter une nouvelle facture ===
st.sidebar.header("Ajouter une nouvelle facture")

with st.sidebar.form("form_ajout_facture"):
    date = st.date_input("Date")
    num_facture = st.text_input("Numéro de Facture")
    description = st.text_input("Description")
    montant_ttc = st.number_input("Montant TTC", min_value=0)
    statut = st.selectbox("Statut", ["Payée", "En attente"])
    fichier_pdf = st.file_uploader("Téléverser le fichier PDF", type=["pdf"])

    # Bouton pour ajouter la ligne
    submit_button = st.form_submit_button(label="Ajouter")

    # Si le bouton est cliqué, ajouter la ligne au DataFrame
    if submit_button:
        if fichier_pdf is not None:
            # Enregistrer le fichier PDF dans le dossier pdf_factures
            pdf_filename = f"{num_facture}.pdf"
            pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
            with open(pdf_path, "wb") as f:
                f.write(fichier_pdf.read())

            # Ajouter la nouvelle ligne au DataFrame
            new_data = {
                "Date": date,
                "Numéro de Facture": num_facture,
                "Description": description,
                "Montant TTC": montant_ttc,
                "Statut": statut,
                "Fichier PDF": pdf_filename
            }
            
            # Correction ici : Utilisation de pd.concat() au lieu de append()
            new_row = pd.DataFrame([new_data])
            achats_df = pd.concat([achats_df, new_row], ignore_index=True)
            
            st.success("Nouvelle facture ajoutée avec succès !")

# === Affichage du tableau des achats ===
st.subheader("Tableau des Achats")
st.dataframe(achats_df)

# === Aperçu intégré des PDF ===
st.subheader("Aperçu des Factures PDF")
for i, row in achats_df.iterrows():
    st.markdown(f"### {row['Numéro de Facture']} - {row['Description']}")
    pdf_file = row["Fichier PDF"]
    pdf_path = os.path.join(PDF_FOLDER, pdf_file)

    # Vérifie si le fichier PDF existe
    if os.path.exists(pdf_path):
        # Affiche le PDF directement dans l'application
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            st.download_button(label="Télécharger le PDF", data=pdf_data, file_name=pdf_file)
            st.markdown(f"#### Aperçu de {pdf_file}")
            st.markdown(f'<iframe src="{pdf_path}" width="700" height="500"></iframe>', unsafe_allow_html=True)
    else:
        st.warning(f"Fichier PDF introuvable pour {row['Numéro de Facture']}")

# === Exportation du tableau en Excel ===
st.sidebar.header("Exporter le tableau")
if st.sidebar.button("Exporter en Excel"):
    achats_df.to_excel("tableau_achats.xlsx", index=False)
    st.sidebar.success("Fichier Excel exporté avec succès !")
