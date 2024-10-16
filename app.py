# Instalação de pacotes necessários (executar apenas uma vez)
"""
pip install selenium webdriver-manager fpdf
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from fpdf import FPDF

# Configuração do serviço do ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # Abrir a página do Google
    driver.get('https://google.com')

    # Esperar a página carregar
    time.sleep(1)

    # Pesquisar o valor do dólar
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'APjFqb'))  # Campo de pesquisa
    )
    search_box.click()
    search_box.send_keys("dolar hoje")
    search_box.send_keys(Keys.RETURN)

    # Capturar o valor do dólar
    dollar_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]"))
    )
    dollar_value = dollar_element.get_attribute("data-value")
    dollar_value_float = float(dollar_value)
    print("=" * 30)
    print("Dólar = R$ {:.2f}".format(dollar_value_float))

    time.sleep(1)

    # Pesquisar o valor do euro
    searc = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='APjFqb']"))
    )
    searc.click()
    searc.clear()
    searc.send_keys("euro hoje")  # escreve texto da nova pesquisa
    searc.send_keys(Keys.RETURN)

    # Capturar o valor do euro
    euro_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]"))
    )
    euro_value = euro_element.get_attribute("data-value")
    euro_value_float = float(euro_value)
    print("Euro = R$ {:.2f}".format(euro_value_float))

    time.sleep(1)

finally:
    # Fechar o navegador
    driver.quit()

# Criação do PDF com os valores obtidos
try:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)

    # Adicionando título ao PDF
    pdf.cell(200, 10, txt="Câmbio Hoje", ln=True, align='L')

    # Mensagens com os valores
    dollar_message = f"O valor do dólar hoje é R$ : R$ {dollar_value_float:.2f}"
    euro_message = f"O valor do euro hoje é R$ : R$ {euro_value_float:.2f}"

    # Adicionando valores ao PDF
    pdf.cell(0, 10, txt=dollar_message, ln=True, align='L')
    pdf.cell(0, 10, txt=euro_message, ln=True, align='L')

    # Salvando o PDF
    pdf.output("valor_cambio.pdf")
    print("PDF criado com sucesso!")

finally:
    print("=" * 30)
    print("        FIM DA EXECUÇÃO          ")
    print("=" * 30)
