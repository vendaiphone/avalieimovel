
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Configurações da página
st.set_page_config(page_title="AvalieJá - Valor do m²", layout="centered")

# Estilo customizado
st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Segoe UI', sans-serif;
        }
        .logo {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .logo img {
            height: 80px;
        }
        .title {
            text-align: center;
            color: #2c3e50;
            font-size: 40px;
            font-weight: bold;
        }
        .sub {
            text-align: center;
            font-size: 18px;
            color: #7f8c8d;
            margin-bottom: 30px;
        }
        .stButton>button {
            background-color: #27ae60;
            color: white;
            font-weight: bold;
            border-radius: 10px;
        }
        .stTextInput>div>input {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Logo fictícia (poderia ser trocada por imagem real hospedada)
st.markdown('<div class="logo"><img src="https://img.icons8.com/external-flat-juicy-fish/60/000000/external-real-estate-location-flat-flat-juicy-fish.png"/></div>', unsafe_allow_html=True)
st.markdown('<div class="title">AvalieJá</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Descubra o valor médio do metro quadrado na sua região</div>', unsafe_allow_html=True)

# Formulário
tipo_imovel = st.selectbox("Tipo de imóvel:", ["Apartamento", "Casa com terreno", "Terreno"])
estado = st.text_input("Estado (sigla, ex: SC):", "SC")
cidade = st.text_input("Cidade:", "Joinville")
bairro = st.text_input("Bairro:", "Glória")
metragem = st.number_input("Metragem do imóvel (m²):", 30, 1000, 84)

if st.button("Calcular valor do m²"):
    min_m2 = metragem - 10
    max_m2 = metragem + 10
    tipo_url = "apartamento"
    if tipo_imovel == "Casa com terreno":
        tipo_url = "casa"
    elif tipo_imovel == "Terreno":
        tipo_url = "terreno"

    url = f"https://www.olx.com.br/imoveis/estado-{estado.lower()}?q={tipo_url}%20{bairro}%20{cidade}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    prices = soup.find_all("span", string=re.compile(r"R\$"))
    data = []
    for i in range(min(len(prices), 10)):
        try:
            valor = prices[i].text.strip()
            valor_num = int(re.sub(r"[^\d]", "", valor))
            m2_simulado = metragem - 5 + i
            if min_m2 <= m2_simulado <= max_m2:
                data.append({"valor (R$)": valor_num, "metragem (m²)": m2_simulado})
        except:
            continue

    if data:
        df = pd.DataFrame(data)
        df["valor médio m² (R$)"] = (df["valor (R$)"] / df["metragem (m²)"]).round(2)
        media_m2 = int(df["valor médio m² (R$)"].mean())

        st.success(f"Valor médio do m² em **{bairro}, {cidade} ({estado})** para **{tipo_imovel}**: R$ {media_m2:,}")
        st.markdown("### Imóveis usados no cálculo:")
        st.dataframe(df)
    else:
        st.warning("Não foram encontrados imóveis suficientes para calcular.")
