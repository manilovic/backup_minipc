from flask import Flask, request, jsonify, render_template, render_template_string
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
from elasticsearch import Elasticsearch
import requests
import os
import subprocess
from busquedaTV import buscar_programas



app = Flask(__name__)

es = Elasticsearch("http://192.168.1.46:9200")    # Crear instancia del cliente de Elasticsearch
 

def save_to_elasticsearch_unique(name, link):
    doc_id = link  # usar el link como ID único
    doc = {
        "name": name,
        "link": link,
    }


    # Verificar si ya existe
    if es.exists(index="acestreams", id=doc_id):
        print(f"Ya existe: {name} : {link}")
    else:
        es.index(index="acestreams", id=doc_id, body=doc)
        print(f"Guardado nuevo: {link}")

def extraer_enlaces(driver):
    elementos = driver.find_elements(By.TAG_NAME, "a")
    enlaces = []
    for elem in elementos:
        href = elem.get_attribute("href")
        if href and ('/pelicula/' in href or '/serie/' in href):
            enlaces.append(href)
    return enlaces


def crear_driver_headless():
    options = uc.ChromeOptions()
    options.add_argument("--headless")  # o simplemente "--headless"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")

    driver = uc.Chrome(options=options, version_main=137, use_subprocess=True)  ########version chromeee
    return driver


def descargar_torrent(url):
    response = requests.get(url)
    torrent_data = response.content  # esto contiene los bytes del .torrent
    filename = os.path.basename(url)  # esto da 'The_Big_Bang_Theory_10_720p_01.torrent'
    with open(filename, "wb") as f:
        f.write(torrent_data)
        print(f"✅ Guardado como: {filename}")
    return (filename)

def get_service_status(service_name):
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip() == "active"
    except Exception:
        return False


@app.route('/')
def home():

    services = {
        "acestream-server": get_service_status("acestream-server.service"),
        "deluged": get_service_status("deluged.service"),
        "deluge-web": get_service_status("deluge-web.service")
    }

    return render_template_string('''
    <h1>Extracción de enlaces de AceStreamSearch</h1>
    <form action="/buscar" method="get">
        <input type="text" name="q" placeholder="Escribe lo que quieres buscar">
        <input type="submit" value="Buscar">
    </form>
    <a href="/listar"><button>Ver links almacenados</button></a>
    
    <br><br>

    <h1> Listar Registros Elastic </h1>
    <form action="/listar_pelis" method="get">
        <input type="submit" value="Ver registros peliculas">
    </form>
    <form action="/listar_series" method="get">
        <input type="submit" value="Ver registros series">
    </form>
    
    <br><br>

    <h1>Buscador enlaces Dontorrent (España)</h1>
    <form action="/dontorrent" method="get">
        <input type="text" name="don" placeholder="Escribe">
        <input type="submit" value="Buscar">
    </form>

    <br><br>
    
    <h1>Búsqueda Programación Movistar Plus</h1>
    <form action="/movistar" method="get">
        <input type="text" name="q" placeholder="Palabras clave (ej: Laliga)">
        <input type="number" name="dias" min="1" max="7" value="1">
        <input type="submit" value="Buscar">
    </form>

    <br><br>
    <h1>Estado de Servicios</h1>
    <ul>
        {% for name, status in services.items() %}
            <li>
                {{ name }}:
                <span style="display:inline-block; width:15px; height:15px; border-radius:50%%; background-color:{{ 'green' if status else 'red' }};"></span>
            </li>
        {% endfor %}
    </ul>

    <br><br>
    

    <form action="/alba" method="get">
      <button type="submit" style="font-size: 40px; padding: 20px 40px;">
        👋 PINCHA AQUI
      </button>
    </form>
    ''', services=services)


@app.route('/buscar')
def get_streams():
    query = request.args.get('q', 'sports')
    url = f'https://acestreamsearch.net/en/?q={query}&v=1'          #### http://localhost:5000/buscar?q=sports
    print(url)

    driver = crear_driver_headless()
    driver.get(url)
    time.sleep(5)  # Esperar a que el contenido JS cargue

    page_source_text = driver.page_source   # Obtener el texto completo de la página

    matches = re.finditer(r"acestream://[a-zA-Z0-9]{40}", page_source_text)

    result = []

    for match in matches:
        acelink = (match.group())
        acelink = acelink[12:]  # Quitar los 12 primeros caracteres

        start = page_source_text.find('>', match.end())
        start = start + 1
        end = page_source_text.find('<', start)
        tv = page_source_text[start:end]
            
        linea =  {"name": tv, "link": acelink}

        result.append(linea)
        save_to_elasticsearch_unique(tv,acelink)




    driver.quit()

    return jsonify(result)  # Sin duplicados


@app.route('/listar')
def list_streams():

    # Buscar en el índice "mi_indice" (ajustalo al tuyo)
    resultado = es.search(index="acestreams", body={"size": 1000,"query": {"match_all": {}}})
    

    # Extraer los documentos
    documentos = [hit["_source"] for hit in resultado["hits"]["hits"]]

    documentos.sort(key=lambda x: x.get("name", "").lower())
    return render_template("tabla.html", documentos=documentos)

    #return render_template("tabla.html", documentos=documentos)
    #return documentos


@app.route('/listar_pelis')
def list_pelis():

    # Buscar en el índice "mi_indice" (ajustalo al tuyo)
    resultado = es.search(index="peliculas_pro", body={"size": 1000,"query": {"match_all": {}}})
    

    # Extraer los documentos
    documentos = [hit["_source"] for hit in resultado["hits"]["hits"]]


    return render_template("tabla.html", documentos=documentos)
    #return documentos


@app.route('/listar_series')
def list_series():

    # Buscar en el índice "mi_indice" (ajustalo al tuyo)
    resultado = es.search(index="series_pro", body={"size": 1000,"query": {"match_all": {}}})

    # Extraer los documentos
    documentos = [hit["_source"] for hit in resultado["hits"]["hits"]]


    return render_template("tabla.html", documentos=documentos)
    #return documentos


@app.route('/dontorrent')
def buscar_dontorrent():

    search_url = "https://t.me/s/DonTorrent"
    driver =  crear_driver_headless()

    driver.get(search_url)

    elementos = driver.find_elements(By.CSS_SELECTOR, 'div.tgme_widget_message_text')

    for elemento in elementos:
        texto = elemento.text
        if "Disponible" in texto:
            base_url = elemento.find_element(By.TAG_NAME, "a").get_attribute("href")
            print(base_url)

    query = request.args.get('don', 'error')  ## q del boton
    search_url = f"{base_url}buscar/{query.replace(' ', '%20')}"
    print(f"Busqueda: {search_url}")

    driver.get(search_url)
    time.sleep(5)  # Esperar a que cargue el contenido dinámico

    paginacion = driver.find_elements(By.CSS_SELECTOR, "li.page-item a.page-link")  

    # 1. Recolectar todas las URLs de paginación primero (como strings)
    paginas = set()
    for link in paginacion:
        href = link.get_attribute("href")
        print(href)
        if href and "/page/" in href:
            paginas.add(href)

    # 2. Agregar también la URL inicial (por si no está incluida)
    paginas.add(search_url)

    enlaces = []

    for pagina in paginas:
        print(f"page: {pagina}")
        driver.get(pagina)
        time.sleep(3)
        enlaces.extend(extraer_enlaces(driver))  # Se añaden a enlaces


    driver.quit()

    return render_template_string('''
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;"> Volver al inicio </a>
        <h1>Resultados de la búsqueda</h1>
        {% for enlace in enlaces %}
            <p><a href="/enviar_a_deluge?url={{ enlace }}" target="_blank">{{ enlace }}</a></p>
        {% endfor %}
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;"> Volver al inicio </a>
    ''', enlaces=enlaces)


@app.route('/enviar_a_deluge')
def enviar_a_deluge():
    url = request.args.get('url')
    if not url:
        return "Falta parámetro 'url'", 400

    try:

        driver = crear_driver_headless()
        driver.get(url)
        time.sleep(5)  # Esperar a que cargue el contenido dinámico


        enlace = driver.find_elements(By.XPATH, "//a[contains(@href, '.torrent')]")

        for enl in enlace:
            url_torrent = enl.get_attribute('href')
            print(url_torrent)
            filename = descargar_torrent(url_torrent)
            
            ruta = f"/home/minipc/acestream-server/{filename}"    # Ruta al archivo .torrent
            with open(ruta, "rb") as f:
                torrent_data = f.read()
                resultado = subprocess.run(['deluge-console', f'add "{ruta}"'],capture_output=True, text=True, check=True)

                
        return "¡Enviado a Deluge!"

    except Exception as e:
        return f"Error: {e}", 500



@app.route('/movistar')
def buscar_movistar():
    palabras = request.args.get('q', '')
    dias = int(request.args.get('dias', '1'))

    if not palabras.strip():
        return "Falta parámetro 'q' (palabras clave)", 400

    lista = [p.strip().lower() for p in palabras.split()]
    resultados = buscar_programas(lista, dias)

    return render_template_string('''
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;"> Volver al inicio </a>
        <h1>Resultados de Movistar Plus</h1>
        {% for r in resultados %}
            <p>{{ r }}</p>
        {% endfor %}
        <a href="/" style="display: inline-block; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px;"> Volver al inicio </a>
    ''', resultados=resultados)


@app.route('/get_magnets', methods=['GET'])
def get_magnets():
    # Configuración de Chrome para Selenium
    options = uc.ChromeOptions()
    # NO USAMOS HEADLESS por ahora
    # options.add_argument("--headless")  # Comentado
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Crear el driver
    driver = uc.Chrome(options=options)
    driver.get("https://btdig.com/search?q=fgt+ghost+protocol")
    time.sleep(10)  # Esperamos más tiempo para cargar la página

    enlaces = []
    magnet_elements = driver.find_elements(By.CSS_SELECTOR, "div.fa-magnet a")
    for elem in magnet_elements:
        href = elem.get_attribute("href")
        if href and href.startswith("magnet:"):
            enlaces.append(href)

    driver.quit()

    # Devolver los enlaces como respuesta JSON
    return jsonify(enlaces)


@app.route('/alba')
def alba():

    return render_template_string('''
    '<p style="font-size: 72px;">ALBA 5 🖐</p>'
    <h1>Imagen local</h1>
        <img src="{{ url_for('static', filename='jm_alba.png') }}" alt="Imagen local" width="720">
    <h1>
    ''')   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
