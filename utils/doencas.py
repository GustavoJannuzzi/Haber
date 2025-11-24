# utils/doencas.py

import streamlit as st

def get_doencas():
    return {
        "Mossaic Virus": {
            "nome_cientifico": "Vírus do Mosaico",
            "descricao": "Causa manchas amareladas irregulares nas folhas (efeito mosaico), levando à queda da produtividade.",
            "agrot": "Não há tratamento químico direto contra vírus.",
            "cuidados": [
                "Uso de sementes certificadas e livres do vírus",
                "Controle de vetores como **pulgões** (ex: *Imidacloprido*)",
                "Eliminar plantas daninhas hospedeiras"
            ]
        },
        "Southern Blight": {
            "nome_cientifico": "Sclerotium rolfsii",
            "descricao": "Apodrecimento na base da planta com presença de micélio branco e escleródios.",
            "agrot": "Fungicidas à base de **Fluazinam**, **Thiabendazole** ou **Azoxystrobina**.",
            "cuidados": [
                "Rotação de culturas",
                "Boa drenagem do solo",
                "Evitar plantio direto sobre palhada contaminada"
            ]
        },
        "Sudden Death Syndrome": {
            "nome_cientifico": "Fusarium virguliforme",
            "descricao": "Clorose entre nervuras e necrose das folhas. Raízes afetadas.",
            "agrot": "Tratamento de sementes com **Fluopyram** ou **Ilevo® (fluopyram + metalaxil)**.",
            "cuidados": [
                "Rotação de culturas",
                "Cultivares resistentes",
                "Evitar solos compactados e excesso de umidade"
            ]
        },
        "Yellow Mosaic": {
            "nome_cientifico": "Vírus do Mosaico Amarelo da Soja",
            "descricao": "Amarelecimento das folhas com padrão em mosaico, transmitido por **mosca-branca**.",
            "agrot": "Controle com **Acetamiprido**, **Bifentrina** ou **Imidacloprido**.",
            "cuidados": [
                "Controle do vetor",
                "Plantio de variedades tolerantes",
                "Eliminação de plantas voluntárias"
            ]
        },
        "Bacterial Blight": {
            "nome_cientifico": "Pseudomonas savastanoi pv. glycinea",
            "descricao": "Manchas angulares nas folhas com aparência oleosa, evoluindo para necrose.",
            "agrot": "Sem controle curativo direto. **Cúpricos** podem ser usados preventivamente.",
            "cuidados": [
                "Evitar sementes infectadas",
                "Rotação de culturas",
                "Evitar irrigação por aspersão"
            ]
        },
        "Brown Spot": {
            "nome_cientifico": "Septoria glycines",
            "descricao": "Pequenas manchas marrons nas folhas, que coalescem em lesões maiores.",
            "agrot": "**Trifloxistrobina**, **Azoxystrobina**, **Picoxystrobina**.",
            "cuidados": [
                "Tratamento de sementes",
                "Aplicação preventiva de fungicidas",
                "Monitoramento no início do ciclo"
            ]
        },
        "Crestamento": {
            "nome_cientifico": "Cercospora kikuchii",
            "descricao": "Manchas avermelhadas nas folhas e vagens, podendo afetar sementes.",
            "agrot": "**Mancozebe**, **Tebuconazol**, **Fluxapiroxade**.",
            "cuidados": [
                "Uso de sementes tratadas",
                "Rotação de culturas",
                "Pulverizações entre R1 e R3"
            ]
        },
        "Ferrugem": {
            "nome_cientifico": "Phakopsora pachyrhizi",
            "descricao": "Manchas marrons e ferruginosas com esporulação abundante. Altamente severa.",
            "agrot": "**Triazóis (Tebuconazol)**, **Estrobilurinas (Azoxystrobina)**, **Carboxamidas (Fluxapiroxade)**.",
            "cuidados": [
                "Aplicações preventivas baseadas em alertas",
                "Cultivares precoces",
                "Eliminar sojas voluntárias no vazio sanitário"
            ]
        },
        "Powdery Mildew": {
            "nome_cientifico": "Microsphaera diffusa",
            "descricao": "Pó branco nas folhas, reduzindo a fotossíntese e produtividade.",
            "agrot": "**Enxofre**, **Protioconazol**, **Azoxystrobina**.",
            "cuidados": [
                "Aplicações preventivas em clima seco",
                "Evitar superpopulação de plantas"
            ]
        },
        "Septoria": {
            "nome_cientifico": "Septoria sojae",
            "descricao": "Lesões circulares e escurecidas nas folhas, similares ao brown spot.",
            "agrot": "**Clorotalonil**, **Mancozebe**, **Trifloxistrobina**.",
            "cuidados": [
                "Monitoramento na fase vegetativa",
                "Controle químico preventivo",
                "Rotação de culturas"
            ]
        },
    }

def exibir_doenca(nome, doenca):
    st.markdown(f"""
    <div style="border:1px solid #333; border-radius:10px; padding:20px; margin-bottom:20px; background-color:#121212; color:#d1d1d1">
        <h4 style="color:#76ff03;">🌱 <b>{nome}</b> <span style="font-weight:normal; color:#999;">({doenca['nome_cientifico']})</span></h4>
        <ul>
            <li><b>🧾 Descrição:</b> {doenca['descricao']}</li>
            <li><b>💊 Agrotóxico:</b> {doenca['agrot']}</li>
            <li><b>🛡️ Cuidados:</b>
                <ul>
                    {''.join([f"<li>{c}</li>" for c in doenca['cuidados']])}
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
