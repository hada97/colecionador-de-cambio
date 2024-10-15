"""   
pip install selenium
pip install webdriver-manager
pip install fpdf

"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import smtplib
from email.mime.text import MIMEText
from fpdf import FPDF

servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome()


try:
    # Abrir a página do ITSM
    driver.get('https://google.com')  # Altere para a URL do seu site ITSM

    # Esperar um pouco para garantir que a página carregue
    time.sleep(1)

    # Procurar elemento por ID
    barrapesq = driver.find_element(By.ID, 'APjFqb')  # Altere para o ID do elemento desejado
    barrapesq.click()  # Exemplo de clicar no elemento
    barrapesq.send_keys("dolar hoje") #escreve texto dentro do campo
    barrapesq.send_keys(Keys.RETURN) #simula o enter
    dolar = driver.find_element("xpath", "//*[@id='knowledge-currency__updatable-data-column']/div[1]/div[2]/span[1]")
    valordolar = dolar.get_attribute("data-value")
    print("Dolar = R$ "+valordolar)
    time.sleep(100)


finally:
    # Fechar o navegador
    driver.quit()


try:
    # Criação do PDF
    pdf = FPDF()
    pdf.add_page()

    # Definindo fonte
    pdf.set_font("Arial", size=24)

    # Adicionando um título
    pdf.cell(200, 10, txt="Valor do Dólar", ln=True, align='C')

    # Adicionando o valor do dólar
    mensagem = f"O valor do dólar hoje é: {valordolar}"
    pdf.cell(200, 10, txt=mensagem, ln=True, align='C')

    # Salvando o PDF
    pdf.output("valor_dolar.pdf")
    print("-----------------------")
    print("PDF criado com sucesso!")

 
finally:
    print("-----------------------")
    print("----FIM DA EXECUCAO----")
    print("-----------------------")
    
  




""" 
# Configurações do email
de = "oi@gmail.com"
para = "oi@gmail.com"
senha = "senha"  # Tenha cuidado ao armazenar senhas
assunto = "Valor do Dólar Hoje"
mensagem = f"O valor do dólar hoje é: {valordolar}"

# Cria o corpo do email
msg = MIMEText(mensagem)
msg['Subject'] = assunto
msg['From'] = de
msg['To'] = para

# Envia o email
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(de, senha)
        server.sendmail(de, para, msg.as_string())
    print("Email enviado com sucesso!")
except Exception as e:
    print(f"Erro ao enviar o email: {e}")"""

