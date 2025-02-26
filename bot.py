from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# 🔹 Configuração do WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# 🔹 Criação do Service
service = Service(ChromeDriverManager().install())

# 🔹 Inicia o navegador com o serviço e opções configuradas
driver = webdriver.Chrome(service=service, options=options)

# 🔹 Acessa o Instagram
driver.get("https://www.instagram.com/")
time.sleep(3)  # Espera a página carregar

# 🔹 Localiza os campos de login
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

# 🔹 Insere as credenciais
username_input.send_keys("rafhenry_")
password_input.send_keys("rafaelgamer100")
password_input.send_keys(Keys.RETURN)

time.sleep(10)  # Aguarda o login ser concluído

print("Login realizado com sucesso!")

# 🔹 Acessa a página de Close Friends
driver.get("https://www.instagram.com/accounts/close_friends/")
time.sleep(5)

# 🔹 Verificando os usuários na lista de Close Friends
try:
    # Localiza todos os ícones de Close Friends
    icons = driver.find_elements(By.XPATH, "//div[@data-bloks-name='ig.components.Icon']")

    for icon in icons:
        # Verifica se o ícone é o que representa "adicionado aos Close Friends"
        if 'circle-check__filled' in icon.get_attribute('style'):
            #print("Usuário já está nos Close Friends!")
            pass
        elif 'circle__outline' in icon.get_attribute('style'):
            print("Usuário NÃO está nos Close Friends!")
            
            # Localiza e clica no ícone que representa o botão de adicionar
            add_button = icon.find_element(By.XPATH, "..")  # Se o ícone for filho de um botão, usa o caminho para o elemento pai
            add_button.click()  # Clica para adicionar o usuário
            print("Usuário adicionado aos Close Friends!")
            
            # Atraso de 30 segundos entre os cliques
            time.sleep(30)
        else:
            print("Ícone não reconhecido.")

except Exception as e:
    print(f"Erro: {e}")

# 🔹 Fecha o navegador após a execução
time.sleep(10)
driver.quit()