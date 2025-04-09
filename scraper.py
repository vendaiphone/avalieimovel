
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

def buscar_imoveis(tipo, cidade, bairro, metragem):
    min_m2 = int(metragem) - 10
    max_m2 = int(metragem) + 10
    resultados = []

    # Configurar o Selenium com Chrome headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    # Montar a URL para o Viva Real
    cidade_formatada = cidade.lower().replace(" ", "-")
    bairro_formatado = bairro.lower().replace(" ", "-")
    url = f"https://www.vivareal.com.br/venda/{tipo}/{cidade_formatada}/{bairro_formatado}/?q={tipo}&areaInicial={min_m2}&areaFinal={max_m2}"
    
    driver.get(url)
    time.sleep(5)

    cards = driver.find_elements(By.CLASS_NAME, "property-card__container")
    for card in cards[:30]:
        try:
            preco = card.find_element(By.CLASS_NAME, "property-card__price").text
            area = card.find_element(By.CLASS_NAME, "property-card__detail-area").text
            link = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            resultados.append({
                "Preço": preco,
                "Área": area,
                "Link": link
            })
        except Exception:
            continue

    driver.quit()
    return pd.DataFrame(resultados)
