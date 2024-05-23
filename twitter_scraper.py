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

    # Intentar hacer clic en el botón "Mostrar más comentarios" varias veces
    while True:
        try:
            show_more_button = driver.find_element(By.XPATH, '//button[@role="button" and .//span[contains(text(), "Mostrar más respuestas")]]')
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(3)  # Esperar a que se carguen los comentarios adicionales
        except NoSuchElementException:
            break

    body = driver.find_element(By.TAG_NAME, 'body')
    for _ in range(10):  # Ajusta el rango según la cantidad de comentarios
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(2)

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