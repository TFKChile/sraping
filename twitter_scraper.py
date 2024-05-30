import time
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

# Iniciar sesión en Twitter
def login_twitter(driver, login_url):
    driver.get(login_url)
    print("Por favor, inicia sesión manualmente en Twitter.")
    time.sleep(150)  
# Navegar al tweet y extraer comentarios
def Extraer_Comentarios(driver, tweet_url, output_file):
    try:
        driver.get(tweet_url)
        time.sleep(2)  # Esperar a que la página del tweet se cargue completamente
    except Exception as e:
        print(f"Error al navegar a la URL del tweet: {e}")
        driver.quit()
        exit()

    body = driver.find_element(By.TAG_NAME, 'body')
    last_height = driver.execute_script("return document.body.scrollHeight")
    last_comment_count = 0
    max_attempts = 3  # Número máximo de intentos sin cambios
    attempts = 0

    while attempts < max_attempts:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

        new_height = driver.execute_script("return document.body.scrollHeight")
        comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
        new_comment_count = len(comments)

        if new_height == last_height and new_comment_count == last_comment_count:
            attempts += 1
        else:
            attempts = 0  # Restablecer el contador si hay cambios
            last_height = new_height
            last_comment_count = new_comment_count

    # Extraer los comentarios
    try:
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