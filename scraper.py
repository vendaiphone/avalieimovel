
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

def buscar_imoveis(tipo, cidade, bairro, metragem):
    min_m2 = int(metragem) - 10
    max_m2 = int(metragem) + 10
    resultados = []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    url_olx = f"https://www.olx.com.br/imoveis/{cidade.lower().replace(' ', '-')}/?q={tipo}&pe={max_m2}&ps={min_m2}"
    driver.get(url_olx)
    time.sleep(3)

    anuncios = driver.find_elements(By.CLASS_NAME, "_2qv_b")
    for a in anuncios[:20]:
        try:
            preco = a.find_element(By.CLASS_NAME, "_3Foba").text
            descricao = a.find_element(By.CLASS_NAME, "_2tW1I").text
            link = a.find_element(By.TAG_NAME, "a").get_attribute("href")
            resultados.append({"descrição": descricao, "preço": preco, "link": link})
        except:
            continue

    driver.quit()
    return pd.DataFrame(resultados)
