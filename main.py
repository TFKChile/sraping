from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from cookies import save_cookies, load_cookies
from twitter_scraper import login_twitter, Extraer_Comentarios

# Ruta para almacenar las cookies
cookies_path = 'twitter_cookies.pkl'

def start_scraping(tweet_url, minero):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    except Exception as e:
        print(f"Error al iniciar el ChromeDriver: {e}")
        return

    # Verificar si las cookies existen
    if os.path.exists(cookies_path):
        driver.get('https://twitter.com')
        time.sleep(3)
        load_cookies(driver, cookies_path)
        driver.refresh()
        time.sleep(3)
    else:
        login_twitter(driver, 'https://twitter.com/login')
        save_cookies(driver, cookies_path)

    # Crear un nombre de archivo único basado en la URL del tweet
    tweet_id = tweet_url.split('/')[-1]
    csv_filename = f'comentarios_{tweet_id}.csv'

    Extraer_Comentarios(driver, tweet_url, minero, id_url=None, filename=csv_filename)
    driver.quit()
    print("El scraping se ha completado correctamente.")

if __name__ == "__main__":
    from interfaz import create_gui
    create_gui()
