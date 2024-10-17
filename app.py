"""pip install selenium webdriver-manager fpdf customtkinter"""

import time
import tkinter as tk
import customtkinter
from fpdf import FPDF
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# Lista para armazenar as moedas e cotacoes
entradas = []
cotacao = []


def pesquisar_moeda(driver, moeda):
    search_box = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='APjFqb']"))#Campo de pesquisa
    )
    search_box.click()
    search_box.clear()
    search_box.send_keys(f"{moeda} hoje")
    search_box.send_keys(Keys.RETURN)

    # Capturar o valor
    moeda_element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]"))
    )
    return float(moeda_element.get_attribute("data-value"))



def salvar_texto(event):
    texto = entrada_texto.get()
    if texto:
        entradas.append(texto)
        entrada_texto.delete(0, tk.END)
        print(f'Texto salvo: {texto}')
        print(f'Entradas atuais: {entradas}')
        rotulo_feedback.configure(text=f' "{texto}" salvo com sucesso!') 


def pesquisar():
    print("=" * 30)
    print('Iniciando pesquisa...')
    janela.destroy()


janela = customtkinter.CTk()
janela.title("Câmbio")
janela.geometry("500x200")

rotulo = customtkinter.CTkLabel(janela, text="Digite a(s) Moeda(s) e pressione Enter:")
rotulo.pack(pady=10)

# Definindo a largura da entrada de texto
entrada_texto = customtkinter.CTkEntry(janela, placeholder_text="Digite", width=200)  # Ajuste o valor conforme necessário
entrada_texto.pack(pady=10)

rotulo_feedback = customtkinter.CTkLabel(janela, text="")
rotulo_feedback.pack(pady=10)

button_width = 15
botao_pesquisar = customtkinter.CTkButton(janela, text="Pesquisar", command=pesquisar, width=button_width)
botao_pesquisar.pack(pady=10)

# Vincula a tecla Enter à função salvar_texto
entrada_texto.bind('<Return>', salvar_texto)
janela.mainloop()



try:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Executa o Chrome sem interface gráfica

    # Configuração do serviço do ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://google.com')

    time.sleep(1)

    # Pesquisar e capturar os valores para cada moeda
    for moeda in entradas:
        valor = pesquisar_moeda(driver, moeda)
        cotacao.append(valor)

    # Imprimir as cotações
    for i, moeda in enumerate(entradas):
        print("=" * 30)
        print("{} = R$ {:.2f}".format(moeda, cotacao[i]))

finally:
    driver.quit()



# Criação do PDF com os valores obtidos
try:
    print("=" * 30)
    print("      CRIANDO RELATORIO     ")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=18)

    # Adicionando título ao PDF
    pdf.cell(200, 10, txt="Câmbio R$", ln=True, align='L')

    # Adicionando valores ao PDF usando um loop
    for i, entradas in enumerate(entradas):
        mensagem = f"O valor do {entradas} é R$:  {cotacao[i]:.2f}"
        pdf.cell(0, 10, txt=mensagem, ln=True, align='L')

     # Obter a data atual no formato yyyMMdd
    data_atual = datetime.now().strftime('%Y%m%d')
    nome_arquivo = f"cambio_{data_atual}.pdf"

    # Salvar o PDF
    pdf.output(nome_arquivo)

finally:
    print("=" * 30)
    print("       FIM DA EXECUÇÃO          ")
    print("=" * 30)