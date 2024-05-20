from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Credenciales de Twitter
username = '' #usuario twitter
password = '' #contraseña twitter

# URL del tweet
tweet_url = 'https://x.com/necko/status/1791691950548267393'

# Inicializar el ChromeDriver
try:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
except Exception as e:
    print(f"Error al iniciar el ChromeDriver: {e}")
    exit()

# Navegar a la página de inicio de sesión
driver.get('https://twitter.com/login')
time.sleep(5)  # Esperar a que la página de inicio de sesión se cargue

# Iniciar sesión en Twitter
try:
    username_field = driver.find_element(By.NAME, 'text')
    username_field.send_keys(username)
    username_field.send_keys(Keys.RETURN)
    time.sleep(3)

    password_field = driver.find_element(By.NAME, 'password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)
    
    time.sleep(5)  # Esperar a que el inicio de sesión se complete
except Exception as e:
    print(f"Error al iniciar sesión: {e}")
    driver.quit()
    exit()

# Navegar a la URL del tweet
try:
    driver.get(tweet_url)
    time.sleep(5)  # Esperar a que la página del tweet se cargue completamente
except Exception as e:
    print(f"Error al navegar a la URL del tweet: {e}")
    driver.quit()
    exit()

# Desplazarse hacia abajo para cargar más comentarios
body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(10):  # Ajusta el rango según la cantidad de comentarios
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

# Extraer los comentarios
try:
    comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="reply"] div[lang]')
    with open("comentarios.txt", "w", encoding="utf-8") as file:
        for comment in comments:
            file.write(comment.text + "\n\n")
    print("Comentarios guardados en 'comentarios.txt'.")
except Exception as e:
    print(f"Error al extraer comentarios: {e}")

# Cerrar el navegador
driver.quit()
