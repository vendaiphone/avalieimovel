
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="AvalieJá - Cálculo do m²", layout="centered")
st.markdown(
    '''
    <style>
        .main {
            background-color: #f5f7fa;
        }
        h1 {
            color: #2c3e50;
            font-size: 36px;
        }
        .stButton button {
            background-color: #3498db;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }
    </style>
    ''', unsafe_allow_html=True
)

st.title("AvalieJá - Descubra o valor do m²")

st.markdown("### Preencha os dados do imóvel:")

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

    # Criando a URL da OLX para scraping simples
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
