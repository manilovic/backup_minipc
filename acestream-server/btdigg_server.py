from flask import Flask, request, jsonify, render_template, render_template_string
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import subprocess
import argparse
import threading
import time
import webbrowser
import sys
import os
import signal
from selenium import webdriver
from selenium.webdriver.firefox.options import Options



print("INICIANDO NAVEGADOR...")


def abrir_chrome():

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = uc.Chrome(options=options)
    return driver

def abrir_firefox():
    options = Options()
    #options.add_argument("--headless")  # Si no quieres GUI, o elimínalo si tienes entorno gráfico
    driver = webdriver.Firefox(options=options)
    return driver



parser = argparse.ArgumentParser(description='Script con argumentos')
parser.add_argument('argumentos', nargs='*', help='Lista de argumentos')      # Permite múltiples argumentos sin flags
args = parser.parse_args()          

print(args)

query = " ".join(args.argumentos)    # Une todos los argumentos en un solo string

search_url = f"https://btdig.com/search?q={query.replace(' ', '+')}"
print(search_url)


driver = abrir_chrome()
driver.get(search_url)

#time_sleep(10)

enlaces = []
max_page = 0

while driver.find_elements(By.LINK_TEXT, "Next →") and max_page <6 :
    print("Siguiente existe")

    magnet_elements = driver.find_elements(By.CSS_SELECTOR, "div.fa-magnet a")
    for elem in magnet_elements:
        href = elem.get_attribute("href")
        if href and href.startswith("magnet:"):
            enlaces.append(href)
    driver.find_element(By.LINK_TEXT, "Next →").click()
    max_page +=1

webbrowser.open("http://192.168.1.48:5001")  # o tu IP local si accedes desde otra máquina


####


app = Flask(__name__)


@app.route('/', methods=['GET'])

def get_magnets():
    return render_template_string('''
        <a href="/apagar" style="display: inline-block; padding: 10px 20px; background-color: #FF0000; color: white; text-decoration: none; border-radius: 5px;"> Apagar web </a>
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;"> Volver al inicio </a>
        <h1>Resultados de la búsqueda</h1>
        {% for enlace in enlaces %}
            {% set nombre = enlace.split('dn=')[-1].split('&')[0] | replace('+', ' ') %}
            <p><a href="/enviar_a_deluge?magnet={{ enlace | urlencode }}" target="_blank">{{ nombre }}</a></p>
        {% endfor %}
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;"> Volver al inicio </a>
        ''', enlaces=enlaces)    



@app.route('/enviar_a_deluge')

def enviar_a_deluge():
    magnet = request.args.get('magnet')
    if not magnet:
        return "Falta parámetro 'magnet'", 400

    try:

        resultado = subprocess.run(['deluge-console', f'add {magnet}'],capture_output=True, text=True, check=True)

                
        return "¡Enviado a Deluge!"

    except Exception as e:
        return f"Error: {e}", 500



@app.route('/apagar')

def shutdown_server():
    def delayed_shutdown():
        driver.quit()     
        time.sleep(1)  # Espera para que el navegador reciba la respuesta
        os._exit(0)    # Mata el proceso (más confiable que werkzeug.shutdown)

    threading.Thread(target=delayed_shutdown).start()
    return 'Servidor apagado correctamente.'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)
