# pages/modelo.py

import streamlit as st

#st.set_page_config(page_title="Modelo de Classificação", layout="wide")
def display_content():

    st.title("🤖 Como o Modelo Foi Construído")
    st.markdown("Entenda os conceitos técnicos, matemáticos e o desempenho do modelo de classificação de doenças em folhas de soja.")

    st.header("✅ Objetivo do Modelo")
    st.markdown("""
    Treinar um modelo de **classificação de imagens** para detectar **10 tipos de doenças em folhas de soja**, usando aprendizado de máquina e redes neurais convolucionais.
    """)

    st.header("🧠 Conceitos Técnicos")
    st.subheader("📊 Classificação de Imagens")
    st.markdown("""
    Problema de **aprendizado supervisionado**, onde o modelo aprende a mapear imagens de folhas para rótulos (doenças).
    """)

    st.subheader("🧮 Arquitetura InceptionV3")
    st.markdown("""
    - Rede Neural Convolucional (CNN) com múltiplas convoluções em paralelo.
    - Usada como **extrator de características pré-treinado** no ImageNet.
    - Camadas densas foram adicionadas para adaptar às 10 classes.

    **Camadas principais da CNN:**
    - Convolução: Extrai padrões com filtros
    - Pooling: Reduz dimensionalidade
    - ReLU: Função de ativação \( f(x) = \max(0, x) \)
    - Softmax: Distribuição de probabilidade na saída
    """)

    st.latex(r'''
    \text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j} e^{z_j}}
    ''')

    st.header("🛠️ O que foi feito no código")

    st.subheader("📁 Carregamento do dataset")
    st.markdown("""
    - Imagens organizadas por pasta (1 pasta = 1 classe)
    - Divisão: 85% para treino, 15% para validação
    - Redimensionamento para 224x224 pixels
    """)

    st.subheader("🔁 Aumento de dados")
    st.markdown("""
    Para robustez do modelo, foram aplicadas:
    - Flip horizontal
    - Rotação aleatória
    - Zoom
    - Normalização dos pixels (0 a 1)
    """)

    st.subheader("🧠 Transfer Learning com InceptionV3")
    st.markdown("""
    - Camadas do InceptionV3 congeladas
    - Adicionadas camadas:
        - Global Average Pooling
        - Dense (ReLU)
        - Dropout
        - Dense (softmax com 10 classes)
    """)

    st.subheader("🏋️ Treinamento")
    st.markdown("""
    - **Função de perda:** `categorical_crossentropy`
    - **Otimizador:** RMSprop (lr = 0.0001)
    - **Callbacks:** ModelCheckpoint, EarlyStopping
    - **Épocas:** 30
    """)

    st.subheader("📈 Avaliação")
    st.markdown("""
    - **Acurácia total na validação:** 91.43%
    - **Loss final:** 0.2787
    """)

    st.subheader("🖼️ Visualização de previsões")
    st.markdown("O modelo exibe previsões reais vs. previstas com imagens da validação.")

    st.subheader("📦 Exportação")
    st.markdown("""
    - `.h5` para Keras
    - `.tflite` para dispositivos embarcados
    """)

    st.subheader("🆚 Comparação com ResNet50")
    st.markdown("""
    - **ResNet50:** Acurácia ≈ 92.14%
    - **InceptionV3:** Acurácia ≈ 91.43%
    - InceptionV3 tem **mais parâmetros treináveis** (500k vs 221k)
    """)

    st.header("📊 Desempenho por Classe")

    st.markdown("""
    Abaixo, o desempenho do modelo por classe com base na **matriz de confusão e no classification report**:

    | Classe                  | Precisão | Revocação | F1-Score | Suporte |
    |------------------------|----------|-----------|----------|---------|
    | Mossaic Virus          | 1.00     | 1.00      | 1.00     | 4       |
    | Southern blight        | 1.00     | 1.00      | 1.00     | 8       |
    | Sudden Death Syndrone  | 0.82     | 1.00      | 0.90     | 9       |
    | Yellow Mosaic          | 0.85     | 0.89      | 0.87     | 19      |
    | Bacterial blight       | 0.75     | 1.00      | 0.86     | 12      |
    | Brown spot             | 1.00     | 0.69      | 0.82     | 13      |
    | Crestamento            | 1.00     | 1.00      | 1.00     | 1       |
    | Ferrugen               | 0.93     | 1.00      | 0.97     | 14      |
    | Powdery mildew         | 1.00     | 0.88      | 0.93     | 24      |
    | Septoria               | 0.00     | 0.00      | 0.00     | 1       |

    - **Acurácia geral:** 90%
    - **F1-score médio ponderado:** 0.90
    """)

    st.success("📌 Conclusão: o modelo teve desempenho robusto, mas ainda pode melhorar para classes com poucos exemplos, como 'septoria'.")
