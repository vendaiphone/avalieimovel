
import streamlit as st
from scraper import buscar_imoveis

st.set_page_config(page_title="AvalieJá", layout="wide")

st.title("AvalieJá - Descubra o valor real do metro quadrado")
st.markdown("Forneça os dados abaixo para calcular o valor médio do m²:")

tipo = st.selectbox("Tipo de imóvel", ["apartamento", "casa", "terreno"])
cidade = st.text_input("Cidade", "Joinville")
bairro = st.text_input("Bairro", "Glória")
metragem = st.number_input("Metragem do imóvel", min_value=10, max_value=1000, value=80)

if st.button("Buscar valor do m²"):
    with st.spinner("Buscando imóveis..."):
        df = buscar_imoveis(tipo, cidade, bairro, metragem)
        if not df.empty:
            st.success(f"{len(df)} imóveis encontrados.")
            st.dataframe(df)
        else:
            st.warning("Nenhum imóvel encontrado.")
