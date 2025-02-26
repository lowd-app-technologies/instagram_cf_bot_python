from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import asyncio
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

class Credentials(BaseModel):
    username: str
    password: str

@app.post("/run_selenium/")
async def run_selenium(credentials: Credentials):
    # Configuração do WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.instagram.com/")
        time.sleep(3)

        username_input = driver.find_element(By.NAME, "username")
        password_input = driver.find_element(By.NAME, "password")

        username_input.send_keys(credentials.username)
        password_input.send_keys(credentials.password)
        password_input.send_keys(Keys.RETURN)

        time.sleep(10)

        # Acessa a página de Close Friends
        driver.get("https://www.instagram.com/accounts/close_friends/")
        time.sleep(5)

        icons = driver.find_elements(By.XPATH, "//div[@data-bloks-name='ig.components.Icon']")
        total_adicionados = 0

        for icon in icons:
            if 'circle__outline' in icon.get_attribute('style'):
                add_button = icon.find_element(By.XPATH, "..")
                add_button.click()
                total_adicionados += 1
                time.sleep(30)

        return {"message": "Processo concluído", "usuarios_adicionados": total_adicionados}

    except Exception as e:
        return {"error": str(e)}

    finally:
        driver.quit()

