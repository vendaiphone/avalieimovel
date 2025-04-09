
import streamlit as st

st.set_page_config(page_title="AvalieJá - Valor do m²", layout="centered")

# Estilo CSS básico
st.markdown("""
    <style>
    .titulo {
        font-size: 36px;
        font-weight: bold;
        color: #4F8BF9;
        text-align: center;
        margin-bottom: 10px;
    }
    .subtitulo {
        font-size: 18px;
        color: #555;
        text-align: center;
        margin-bottom: 30px;
    }
    .resultado {
        font-size: 24px;
        color: #009900;
        font-weight: bold;
        text-align: center;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Título e subtítulo
st.markdown('<div class="titulo">📐 AvalieJá</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Descubra o valor médio do metro quadrado do seu imóvel</div>', unsafe_allow_html=True)

# Formulário de entrada
bairro = st.text_input("🏙️ Bairro", "Glória")
cidade = st.text_input("🌆 Cidade", "Joinville")
estado = st.text_input("🗺️ Estado (sigla)", "SC")
metragem = st.number_input("📏 Metragem do imóvel (m²)", min_value=10.0, max_value=1000.0, value=84.0, step=1.0)

# Botão de avaliação
if st.button("🔍 Avaliar valor do m²"):
    # Simulação de scraping e cálculo (MVP)
    valor_total_medio = 470000  # exemplo fixo
    valor_m2 = valor_total_medio / metragem

    st.markdown('<div class="resultado">💰 Valor médio estimado do m²: <br><br>R$ {:,.2f}</div>'.format(valor_m2), unsafe_allow_html=True)
