# pages/historico.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from utils.db_operations import (
    get_all_scans_detailed,
    get_confidence_by_disease,
    get_all_scan_locations
)
from utils.auth import get_user_id

def apply_confidence_gradient(val):
    """Aplica gradiente de verde baseado no valor de confiança"""
    if pd.isna(val):
        return ''
    try:
        # Converte para float se for string
        if isinstance(val, str):
            val = float(val.replace(',', '.'))
        # Normaliza entre 0.80 e 1.0 para ter um range melhor de cores
        normalized = (val - 0.80) / 0.20
        normalized = max(0, min(1, normalized))  # Clamp entre 0 e 1
        # Gradiente do verde claro ao verde escuro
        green_intensity = int(100 + (155 * normalized))
        color = f'rgb(0, {green_intensity}, 0)'
        return f'background-color: {color}; color: white; font-weight: bold;'
    except:
        return ''

def display_content():
    st.title("📊 Histórico de Análises")

    # Obtém o ID do usuário logado
    user_id = get_user_id()
    if not user_id:
        st.error("Usuário não autenticado")
        return

    # Carrega os dados
    with st.spinner("Carregando dados..."):
        scans = get_all_scans_detailed()
        confidence_data = get_confidence_by_disease()
        location_data = get_all_scan_locations()

    if not scans:
        st.info("Nenhuma análise encontrada no histórico.")
        return

    # ===== SEÇÃO 1: HISTÓRICO DAS IDENTIFICAÇÕES =====
    st.markdown("---")
    st.markdown("### 📋 **Histórico das Identificações**")

    # Converte para DataFrame
    df = pd.DataFrame(scans)

    # Formata a data
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%d/%m/%Y %H:%M')

    # Prepara a coluna confidence em formato decimal
    df['confidence_display'] = df['confidence'].apply(lambda x: f"{float(x):.5f}")

    # Seleciona e renomeia as colunas
    display_df = df[['created_at', 'disease_name', 'confidence_display', 'city_name', 'location_source']]
    display_df.columns = ['Data/Hora', 'Doença', 'Confiança', 'Cidade', 'Fonte']

    # Aplica estilo com gradiente de verde
    styled_df = display_df.style.map(
        apply_confidence_gradient,
        subset=['Confiança']
    ).set_properties(**{
        'background-color': '#1E1E1E',
        'color': 'white',
        'border-color': '#2D2D2D'
    })

    st.dataframe(styled_df, use_container_width=True, height=400)

    # ===== SEÇÃO 2: QUANTIDADE POR DOENÇA =====
    st.markdown("---")
    st.markdown("### 📊 **Quantidade por Doença**")

    # Conta quantas vezes cada doença aparece
    disease_counts = df['disease_name'].value_counts().reset_index()
    disease_counts.columns = ['Doença', 'Quantidade']

    # Ordena por quantidade para melhor visualização
    disease_counts = disease_counts.sort_values('Quantidade', ascending=False)

    # Cria gráfico de barras com tons de verde
    fig_counts = go.Figure(data=[
        go.Bar(
            x=disease_counts['Doença'],
            y=disease_counts['Quantidade'],
            marker=dict(
                color=disease_counts['Quantidade'].values,
                colorscale=['#90EE90', '#228B22', '#006400'],  # Verde claro ao escuro
                showscale=False
            ),
            text=disease_counts['Quantidade'].values,
            textposition='outside',
            textfont=dict(color='white', size=12)
        )
    ])

    fig_counts.update_layout(
        paper_bgcolor='#0E1117',
        plot_bgcolor='#1E1E1E',
        font=dict(color='white', size=12),
        xaxis=dict(
            title="",
            tickangle=-45,
            gridcolor='#2D2D2D'
        ),
        yaxis=dict(
            title="Quantidade",
            gridcolor='#2D2D2D'
        ),
        margin=dict(l=40, r=40, t=40, b=100),
        height=400
    )

    st.plotly_chart(fig_counts, use_container_width=True)
    # ===== SEÇÃO 3: CONFIANÇA MÉDIA POR DOENÇA =====
    st.markdown("---")
    st.markdown("### 🎯 **Confiança Média das Identificações por Doença**")

    if confidence_data and len(confidence_data) > 0:
        # Cria DataFrame com dados do banco
        conf_df = pd.DataFrame(confidence_data)

        # Converte Decimal para float de forma EXPLÍCITA
        conf_df['avg_confidence'] = conf_df['avg_confidence'].apply(lambda x: float(x))
        conf_df['count'] = conf_df['count'].apply(lambda x: int(x))

        # Ordena por nome da doença
        conf_df = conf_df.sort_values('disease_name')

        # -------- BOA NORMALIZAÇÃO PARA TAMANHO DAS BOLHAS --------
        min_size = 20
        max_size = 60

        if conf_df['count'].max() > 0:
            conf_df['size'] = min_size + (conf_df['count'] / conf_df['count'].max()) * (max_size - min_size)
        else:
            conf_df['size'] = min_size

        # -------- FIGURA --------
        fig_confidence = go.Figure(
            data=[
                go.Scatter(
                    x=conf_df['disease_name'].values,
                    y=conf_df['avg_confidence'].values,
                    mode='markers+text',
                    marker=dict(
                        size=conf_df['size'].values,
                        color=conf_df['avg_confidence'].values,
                        colorscale=['#A9A9A9', '#90EE90', '#228B22', '#006400'],
                        showscale=True,
                        colorbar=dict(
                            title=dict(text="Confiança", font=dict(color='white')),
                            tickfont=dict(color='white')
                        ),
                        line=dict(width=2, color='white'),
                        sizemode='diameter',
                    ),
                    text=conf_df['count'].astype(int).values,
                    textposition="middle center",
                    textfont=dict(color="white", size=12, family="Arial Black"),
                    customdata=conf_df[['disease_name', 'avg_confidence', 'count']].values,
                    hovertemplate="<b>%{customdata[0]}</b><br>Confiança: %{customdata[1]:.1%}<br>Total: %{customdata[2]} detecções<extra></extra>"
                )
            ]
        )

        # -------- AJUSTES DE LAYOUT --------
        fig_confidence.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#1E1E1E",
            font=dict(color="white"),
            xaxis=dict(
                title="",
                tickangle=-45,
                gridcolor="#2D2D2D"
            ),
            yaxis=dict(
                title="Confiança Média",
                tickformat=".0%",
                gridcolor="#2D2D2D"
            ),
            height=500,
            margin=dict(l=50, r=50, t=40, b=120),
        )

        st.plotly_chart(fig_confidence, use_container_width=True)

        st.markdown("*Tamanho das bolhas representa o número total de detecções*")

    else:
        st.info("Dados insuficientes para exibir confiança média por doença.")

    # ===== SEÇÃO 4: MAPA DE LOCALIZAÇÕES =====
    st.markdown("---")
    st.markdown("### 🗺️ **Mapa de Localizações das Detecções**")

    if location_data and len(location_data) > 0:
        # Cria DataFrame de localizações
        loc_df = pd.DataFrame(location_data)

        # Remove linhas com coordenadas inválidas
        loc_df = loc_df.dropna(subset=['latitude', 'longitude'])

        if len(loc_df) > 0:
            # Define cores para cada doença
            disease_colors = {
                'Mossaic Virus': '#FFD700',
                'Southern Blight': '#FF6347',
                'Sudden Death Syndrome': '#8B4513',
                'Yellow Mosaic': '#FFFF00',
                'Bacterial Blight': '#4169E1',
                'Brown Spot': '#A0522D',
                'Crestamento': '#FF4500',
                'Ferrugem': '#B8860B',
                'Powdery Mildew': '#F0E68C',
                'Septoria': '#2F4F4F'
            }

            # Calcula o centro do mapa (média das coordenadas ou Curitiba como padrão)
            center_lat = loc_df['latitude'].mean() if len(loc_df) > 0 else -25.4284
            center_lon = loc_df['longitude'].mean() if len(loc_df) > 0 else -49.2733

            # Cria o mapa
            m = folium.Map(
                location=[center_lat, center_lon],
                zoom_start=10,
                tiles='CartoDB dark_matter'  # Tema escuro
            )

            # Adiciona marcadores para cada localização
            for idx, row in loc_df.iterrows():
                disease = row['disease_name']
                color = disease_colors.get(disease, '#FFFFFF')

                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=8,
                    popup=f"""
                    <div style='font-family: Arial; font-size: 12px;'>
                        <b>{disease}</b><br>
                        Cidade: {row['city_name'] if row['city_name'] else 'Desconhecida'}<br>
                        Data: {pd.to_datetime(row['created_at']).strftime('%d/%m/%Y %H:%M')}
                    </div>
                    """,
                    color=color,
                    fill=True,
                    fillColor=color,
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)

            # Adiciona legenda
            legend_html = '''
            <div style="position: fixed;
                        top: 10px; right: 10px;
                        background-color: rgba(30, 30, 30, 0.9);
                        border: 2px solid white;
                        border-radius: 5px;
                        padding: 10px;
                        font-size: 12px;
                        color: white;
                        z-index: 9999;">
                <p style="margin: 0 0 5px 0; font-weight: bold;">Legenda:</p>
            '''

            for disease, color in disease_colors.items():
                legend_html += f'<p style="margin: 3px 0;"><span style="background-color: {color}; padding: 2px 8px; border-radius: 3px; color: black; font-weight: bold;">&nbsp;&nbsp;</span> {disease}</p>'

            legend_html += '</div>'

            # Adiciona a legenda ao mapa
            m.get_root().html.add_child(folium.Element(legend_html))

            # Exibe o mapa
            st_folium(m, width=None, height=500)
        else:
            st.info("Nenhuma localização válida encontrada para exibir no mapa.")
    else:
        st.info("Nenhuma localização disponível para exibir no mapa.")

    # Estatísticas gerais no rodapé
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 Total de Análises", len(scans))
    with col2:
        st.metric("🦠 Doenças Detectadas", disease_counts['Doença'].nunique())
    with col3:
        avg_conf = df['confidence'].astype(float).mean()
        st.metric("🎯 Confiança Média", f"{avg_conf:.2%}")
