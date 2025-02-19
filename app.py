import streamlit as st
import pandas as pd
import os

# === Vérifier et installer la bibliothèque openpyxl si absente ===
try:
    import openpyxl
except ImportError:
    os.system("pip install openpyxl")

# === Configuration des fichiers et dossiers ===
EXCEL_FILE = "factures.xlsx"  # Fichier Excel pour sauvegarder les factures
PDF_FOLDER = "pdf_factures"  # Dossier de stockage des fichiers PDF

# Création du dossier pour stocker les fichiers PDF s'il n'existe pas
if not os.path.exists(PDF_FOLDER):
    os.makedirs(PDF_FOLDER)

# === Chargement des données depuis Excel (ou création si inexistant) ===
if os.path.exists(EXCEL_FILE):
    achats_df = pd.read_excel(EXCEL_FILE)
else:
    achats_df = pd.DataFrame(columns=["Date", "Numéro de Facture", "Description", "Montant TTC", "Statut", "Fichier PDF"])

# === Interface de l'application ===
st.title("📑 Gestion des Achats et Factures avec PDF Intégré")

# === Formulaire pour ajouter une nouvelle facture ===
st.sidebar.header("➕ Ajouter une nouvelle facture")

with st.sidebar.form("form_ajout_facture"):
    date = st.date_input("📅 Date")
    num_facture = st.text_input("📝 Numéro de Facture")
    description = st.text_input("📌 Description")
    montant_ttc = st.number_input("💰 Montant TTC", min_value=0)
    statut = st.selectbox("✅ Statut", ["Payée", "En attente"])
    fichier_pdf = st.file_uploader("📂 Téléverser le fichier PDF", type=["pdf"])

    # Bouton pour ajouter la ligne
    submit_button = st.form_submit_button(label="✅ Ajouter la facture")

    # Si le bouton est cliqué, ajouter la ligne au DataFrame
    if submit_button:
        if num_facture and description and montant_ttc and fichier_pdf is not None:
            # Enregistrer le fichier PDF
            pdf_filename = f"{num_facture}.pdf"
            pdf_path = os.path.join(PDF_FOLDER, pdf_filename)
            with open(pdf_path, "wb") as f:
                f.write(fichier_pdf.read())

            # Ajouter la nouvelle ligne au DataFrame
            new_data = {
                "Date": date.strftime("%Y-%m-%d"),
                "Numéro de Facture": num_facture,
                "Description": description,
                "Montant TTC": montant_ttc,
                "Statut": statut,
                "Fichier PDF": pdf_filename
            }
            
            # Mise à jour du DataFrame
            new_row = pd.DataFrame([new_data])
            achats_df = pd.concat([achats_df, new_row], ignore_index=True)
            
            # Sauvegarde des données dans le fichier Excel
            achats_df.to_excel(EXCEL_FILE, index=False)

            st.success("✅ Nouvelle facture ajoutée avec succès !")

        else:
            st.error("⚠️ Veuillez remplir tous les champs et téléverser un fichier PDF.")

# === Affichage du tableau des achats ===
st.subheader("📋 Liste des Factures")
st.dataframe(achats_df)

# === Aperçu des fichiers PDF ===
st.subheader("📑 Aperçu des Factures PDF")
for i, row in achats_df.iterrows():
    st.markdown(f"### {row['Numéro de Facture']} - {row['Description']}")
    pdf_file = row["Fichier PDF"]
    pdf_path = os.path.join(PDF_FOLDER, pdf_file)

    # Vérifie si le fichier PDF existe
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
            st.download_button(label="📥 Télécharger le PDF", data=pdf_data, file_name=pdf_file)
            st.markdown(f"#### 📄 Aperçu de {pdf_file}")
            st.markdown(f'<iframe src="{pdf_path}" width="700" height="500"></iframe>', unsafe_allow_html=True)
    else:
        st.warning(f"⚠️ Fichier PDF introuvable pour {row['Numéro de Facture']}")

# === Exportation du tableau en Excel ===
st.sidebar.header("📂 Exporter le tableau")
if st.sidebar.button("📤 Exporter en Excel"):
    achats_df.to_excel(EXCEL_FILE, index=False)
    st.sidebar.success("✅ Fichier Excel exporté avec succès !")
