import streamlit as st
import pandas as pd
from utils.paragraph_scraper import get_random_paragraph
from utils.openai_api import translate_to_falc, is_valid_api_key
import openai
import os

# Chemin du fichier CSV
CSV_PATH = 'data/falc_translations.csv'

# Initialisation du DataFrame pour enregistrer les résultats
if os.path.exists(CSV_PATH):
    df = pd.read_csv(CSV_PATH)
else:
    data = {
        'Title': [],
        'Original Paragraph': [],
        'FALC Translation': [],
        'FALC OK': []
    }
    df = pd.DataFrame(data)

def load_new_paragraph():
    st.session_state.current_title, st.session_state.current_paragraph = get_random_paragraph()
    if st.session_state.current_title and st.session_state.current_paragraph:
        st.session_state.current_falc_text = translate_to_falc(st.session_state.current_paragraph)
    else:
        st.error("Impossible de récupérer un paragraphe. Réessayez.")

st.title("Traduction FALC de Wikipedia")

# Entrée de la clé API
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''

if st.session_state.api_key == '':
    api_key_input = st.text_input("Entrez votre clé API OpenAI:", type="password")
    if st.button("Valider la clé API"):
        if is_valid_api_key(api_key_input):
            st.session_state.api_key = api_key_input
            st.success("Clé API valide!")
            st.experimental_rerun()
        else:
            st.error("Clé API invalide. Veuillez réessayer.")
else:
    openai.api_key = st.session_state.api_key

    if 'current_title' not in st.session_state:
        load_new_paragraph()

    if st.session_state.current_title:
        st.subheader(f"Article: {st.session_state.current_title}")
        st.write(f"**Paragraphe original:**\n{st.session_state.current_paragraph}")
        st.write(f"**Traduction en FALC:**\n{st.session_state.current_falc_text}")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("OK"):
                new_row = {
                    'Title': st.session_state.current_title,
                    'Original Paragraph': st.session_state.current_paragraph,
                    'FALC Translation': st.session_state.current_falc_text,
                    'FALC OK': 'oui'
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                st.success("Traduction validée.")
                load_new_paragraph()
                st.experimental_rerun()
        with col2:
            if st.button("Non OK"):
                new_row = {
                    'Title': st.session_state.current_title,
                    'Original Paragraph': st.session_state.current_paragraph,
                    'FALC Translation': st.session_state.current_falc_text,
                    'FALC OK': 'non'
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                st.error("Traduction non validée.")
                load_new_paragraph()
                st.experimental_rerun()
        with col3:
            if st.button("Ne sais pas"):
                new_row = {
                    'Title': st.session_state.current_title,
                    'Original Paragraph': st.session_state.current_paragraph,
                    'FALC Translation': st.session_state.current_falc_text,
                    'FALC OK': 'ne sais pas'
                }
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                df.to_csv(CSV_PATH, index=False)
                st.warning("État 'Ne sais pas' enregistré.")
                load_new_paragraph()
                st.experimental_rerun()
        with col4:
            if st.button("Mauvais scrapping"):
                st.error("Paragraphe marqué comme 'Mauvais scrapping'. Aucun enregistrement effectué.")
                load_new_paragraph()
                st.experimental_rerun()
    else:
        load_new_paragraph()
