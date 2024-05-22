import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Iniciar sesión en Twitter
def login_twitter(driver, username, password):
    driver.get('https://twitter.com/login')
    time.sleep(5)  # Esperar a que la página de inicio de sesión se cargue

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

# Navegar al tweet y extraer comentarios
def Extraer_Comentarios(driver, tweet_url, output_file):
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
        # Buscar los comentarios dentro del contenedor
        comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
        
        if not comments:
            print("No se encontraron comentarios con el selector actual.")
        else:
            with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                csvwriter = csv.writer(csvfile)
                for comment in comments:
                    csvwriter.writerow([comment.text])
                    print(comment.text + "\n")
    except Exception as e:
        print(f"Error al extraer comentarios: {e}")
