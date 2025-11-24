# pages/doencas.py

import streamlit as st
from utils.db_operations import get_all_diseases

#st.set_page_config(page_title="Doenças da Soja", layout="wide")
def display_content():
    st.title("🦠 Doenças em Folhas de Soja")
    st.markdown("Aqui você encontra uma descrição breve, agrotóxicos recomendados e os cuidados que o produtor deve ter para cada doença.")

    # Obtém todas as doenças do banco de dados
    diseases = get_all_diseases()
    
    if not diseases:
        st.error("Erro ao carregar informações sobre doenças.")
        return

    for disease in diseases:
        bloco_doenca(
            disease['name'],
            disease['scientific_name'],
            disease['description'],
            disease['treatment'],
            disease['precautions']
        )

def bloco_doenca(titulo, nome_cientifico, descricao, agrot, cuidados):
    st.markdown(f"""
    <div style="border:1px solid #333; border-radius:10px; padding:20px; margin-bottom:20px; background-color:#121212; color:#d1d1d1">
        <h4 style="color:#76ff03;">🌱 <b>{titulo}</b> <span style="font-weight:normal; color:#999;">({nome_cientifico})</span></h4>
        <ul>
            <li><b>🧾 Descrição:</b> {descricao}</li>
            <li><b>💊 Agrotóxico:</b> {agrot}</li>
            <li><b>🛡️ Cuidados:</b>
                <ul>
                    {''.join([f"<li>{c}</li>" for c in cuidados])}
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
