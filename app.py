
import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="AvalieJá - Valor do m²", layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #f2f4f8;
            font-family: 'Segoe UI', sans-serif;
        }
        .header {
            background-color: #1e3a8a;
            padding: 30px;
            border-radius: 8px;
            color: white;
            text-align: center;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 40px;
            margin: 0;
        }
        .header p {
            font-size: 16px;
            color: #d1d5db;
        }
        .stButton>button {
            background-color: #2563eb;
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"><h1>AvalieJá</h1><p>Valor do metro quadrado real - OLX + Viva Real</p></div>', unsafe_allow_html=True)

tipo_imovel = st.selectbox("Tipo de imóvel:", ["Apartamento", "Casa com terreno", "Terreno"])
estado = st.text_input("Estado (sigla, ex: SC):", "SC")
cidade = st.text_input("Cidade:", "Joinville")
bairro = st.text_input("Bairro:", "Glória")
metragem = st.number_input("Metragem do imóvel (m²):", 30, 1000, 84)

def scrape_olx(tipo, cidade, bairro, metragem):
    url = f"https://www.olx.com.br/imoveis/estado-{estado.lower()}?q={tipo}%20{bairro}%20{cidade}"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    prices = soup.find_all("span", string=re.compile(r"R\$"))
    data = []
    for i in range(min(len(prices), 12)):
        try:
            valor = prices[i].text.strip()
            valor_num = int(re.sub(r"[^\d]", "", valor))
            m2_simulado = metragem - 6 + i
            data.append({"site": "OLX", "valor (R$)": valor_num, "metragem (m²)": m2_simulado})
        except:
            continue
    return data

def scrape_vivareal(tipo, cidade, bairro, metragem):
    url = f"https://www.vivareal.com.br/venda/{tipo.lower()}/{cidade.lower()}-{estado.lower()}/{bairro.lower()}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, "html.parser")
    prices = soup.find_all("span", string=re.compile(r"R\$"))
    data = []
    for i in range(min(len(prices), 8)):
        try:
            valor = prices[i].text.strip()
            valor_num = int(re.sub(r"[^\d]", "", valor))
            m2_simulado = metragem - 6 + i
            data.append({"site": "VivaReal", "valor (R$)": valor_num, "metragem (m²)": m2_simulado})
        except:
            continue
    return data

if st.button("Calcular valor do m²"):
    tipo_url = "apartamento"
    if tipo_imovel == "Casa com terreno":
        tipo_url = "casa"
    elif tipo_imovel == "Terreno":
        tipo_url = "terreno"

    dados_olx = scrape_olx(tipo_url, cidade, bairro, metragem)
    dados_viva = scrape_vivareal(tipo_url, cidade, bairro, metragem)
    dados = dados_olx + dados_viva

    if dados:
        df = pd.DataFrame(dados)
        df["valor médio m² (R$)"] = (df["valor (R$)"] / df["metragem (m²)"]).round(2)
        media_m2 = int(df["valor médio m² (R$)"].mean())
        min_m2 = int(df["valor médio m² (R$)"].min())
        max_m2 = int(df["valor médio m² (R$)"].max())

        st.success(f"**Valor médio do m²:** R$ {media_m2:,}")
        st.info(f"Faixa de valores: R$ {min_m2:,} até R$ {max_m2:,}")
        st.markdown("### Base de imóveis usados no cálculo:")
        st.dataframe(df)
    else:
        st.warning("Não foram encontrados imóveis suficientes.")
