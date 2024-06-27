import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import sys
import re
import csv
import os
import unicodedata

def login_twitter(driver, login_url):
    driver.get(login_url)
    print("Por favor, inicia sesión manualmente en Twitter.")
    time.sleep(150)  # Tiempo para iniciar sesión manualmente

def validar_url(linkscrap, minero):
    global id_url_paracom
    id_url_paracom = 1  # Asignamos un ID ficticio para pruebas locales
    print(f"Validación simulada de la URL: {linkscrap} con minero: {minero}")

def clean_text(text):
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn' or c in 'áéíóúñÁÉÍÓÚÑ')
    text = re.sub(r'[^\w\s@]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('\n', ' ')
    return text

def es_duplicado(user_name, comment_text, comment_date, recorded_comments):
    comment_id = (user_name, comment_text, comment_date)
    if comment_id in recorded_comments:
        return True
    else:
        recorded_comments.add(comment_id)
        return False

def limpiar_csv(filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Usuario', 'Comentario', 'Fecha'])

def guardar_comentarios_csv(comentarios, filename):
    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for comentario in comentarios:
            writer.writerow(comentario)

def leer_comentarios_csv(filename):
    comentarios = []
    if os.path.isfile(filename):
        with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar el encabezado
            for row in reader:
                comentarios.append(tuple(row))
    return comentarios

def Extraer_Comentarios(driver, tweet_url, minero, id_url, filename='comentarios.csv'):
    validar_url(tweet_url, minero)

    try:
        driver.get(tweet_url)
        time.sleep(2)
    except Exception as e:
        print(f"Error al navegar a la URL del tweet: {e}")
        driver.quit()
        exit()

    body = driver.find_element(By.TAG_NAME, 'body')
    recorded_comments = set()
    comment_count = 0

    limpiar_csv(filename)
    previous_comment_count = -1
    no_change_attempts = 0

    while no_change_attempts < 3:
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

        try:
            users = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="User-Name"]')
            comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
            dates = driver.find_elements(By.CSS_SELECTOR, 'a > time')

            if not comments:
                print("No se encontraron comentarios con el selector actual.")
            else:
                nuevos_comentarios = []
                for user, comment, date in zip(users, comments, dates):
                    user_name = clean_text(user.find_element(By.CSS_SELECTOR, 'span.css-1jxf684').text.replace('@', ''))
                    comment_text = clean_text(comment.text)
                    comment_date = datetime.strptime(date.get_attribute('datetime'), '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d %H:%M:%S')
                    fecha_add = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    if not es_duplicado(user_name, comment_text, comment_date, recorded_comments) and comment_text:
                        comment_count += 1
                        nuevos_comentarios.append((user_name, comment_text, comment_date))

                guardar_comentarios_csv(nuevos_comentarios, filename)

                if comment_count == previous_comment_count:
                    no_change_attempts += 1
                else:
                    no_change_attempts = 0
                previous_comment_count = comment_count

        except Exception as e:
            print(f"Error al extraer comentarios: {e}")
            no_change_attempts += 1

    print(f"Cantidad total de comentarios registrados: {comment_count}")
