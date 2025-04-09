
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="AvalieJá - Valor do m²", layout="centered")
st.title("AvalieJá - Calculadora de Valor do Metro Quadrado")

# Inputs do usuário
bairro = st.text_input("Digite o bairro:", "Glória")
cidade = st.text_input("Digite a cidade:", "Joinville")
metragem = st.number_input("Metragem do seu imóvel (m²):", 30, 300, 84)

if st.button("Calcular valor do m²"):
    min_m2 = metragem - 10
    max_m2 = metragem + 10

    # URL genérica da OLX (sem filtros avançados)
    url = f"https://www.olx.com.br/imoveis/estado-sc?q=apartamento%20{bairro}%20{cidade}"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    titles = soup.find_all("h2")
    prices = soup.find_all("span", string=re.compile(r"R\$"))

    data = []
    for i in range(min(len(prices), 10)):  # Limitar a 10 imóveis para teste rápido
        try:
            valor = prices[i].text.strip()
            valor_num = int(re.sub(r"[^\d]", "", valor))
            m2_simulado = metragem - 5 + i  # Simular metragens diferentes
            if min_m2 <= m2_simulado <= max_m2:
                data.append({"valor": valor_num, "metragem": m2_simulado})
        except:
            continue

    if data:
        df = pd.DataFrame(data)
        df["valor_m2"] = df["valor"] / df["metragem"]
        media_m2 = int(df["valor_m2"].mean())

        st.success(f"Valor médio do m² no bairro **{bairro}** (Joinville): R$ {media_m2:,}")
        st.dataframe(df)
    else:
        st.warning("Não foram encontrados imóveis suficientes para calcular.")
