import os
import sys
import subprocess
import re
import requests
import json

###  sys.path.append('/media/minipc/HDD/Scripts')  añadirlo al path 
###  for directory in sys.path:
###     print(directory)


def log_updates(programa,mensaje):

    log = "date +'%c || " + programa + " || " + mensaje + " ||'  >> LogsJM/updates.txt "
    subprocess.run(log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def log_monitor(programa,mensaje):

    log = "date +'%c || " + programa + " || " + mensaje + " ||'  >> LogsJM/monitor.txt "
    subprocess.run(log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def create_lock(name):

    filename = f"/tmp/{name}.lock"

    if os.path.exists(filename):
        log_monitor(name,"Script ejecutándose")
        print("Script ejecutándose")
        sys.exit(1)
    else:
        with open(filename, 'w') as filelock:
            filelock.write(f"{name}\n")


def remove_lock(name):

    filename = f"/tmp/{name}.lock"
    os.remove(filename)


def busqueda_serie(line):

    last_part = line.split("/")[-1]   # Divide la línea por '/' y toma la última parte

    patron1 = r"S[0-9]{2}E[0-9]{2}"
    patron2 = r"[0-9]{1}[xX][0-9]{2}"
    patron3 = r"[0-9]{2}[xX][0-9]{2}"
    patron4 = r"Cap [0-9]{3}"
    patron5 = r"Temporarda"
    patron6 = r"HDTV"

    if re.search(patron1, line) or re.search(patron2, line) or re.search(patron3, line) or re.search(patron4, line)or re.search(patron5, line) or re.search(patron6, line):
        log_monitor("Fichero Serie",last_part)
        return("Serie")
    else:
        log_monitor("Fichero Pelicula",last_part)
        return("Pelicula")


def obtener_nombre_pelicula(line):

    nombre_TMDB = re.sub(r'\.[^.]*$', '', line)                                          # Elimina la extensión del archivo
    nombre_TMDB = re.sub(r'\.|\[|\]|\_|\(|\)|\+', ' ', nombre_TMDB)                      # Reemplaza los caracteres especiales por espacio (probando sin quitar el guion "\-" )
    nombre_TMDB = re.split(r'(\s[0-9]{4}\s)|([0-9]{4}p)|([0-9]{3}p)', nombre_TMDB)[0]    # Extrae el título antes de la resolución o el año
    nombre_TMDB = re.split(r'4K|2160p|FullBluRay|FullUHD', nombre_TMDB)[0]               # ISOs
    nombre_TMDB = re.split(r'4K|BD|MicroHD|DVD|M1080|BluRay|Cam|www', nombre_TMDB)[0]    # Elimina términos de calidad de video
    nombre_TMDB = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', nombre_TMDB)                    # Inserta un espacio entre letras y números
    nombre_TMDB = re.sub(r'\s+', '+', nombre_TMDB).strip('+')                            # Reemplaza espacios por "+" y elimina "+" finales
    
    return(nombre_TMDB)


def obtener_nombre_serie(line):

    nombre_TMDB = re.sub(r'\.[^.]*$', '', line)                      # quitamos ext
    nombre_TMDB = re.sub(r'\.|\[|\]|\_|\(|\)|\+', ' ', nombre_TMDB)  # quitamos caraceres raros
    nombre_TMDB = re.split(r'\([0-9]{4}\)', nombre_TMDB)[0]          # filtramos por año (xxxx)
    nombre_TMDB = re.split(r'S[0-9]{2}E[0-9]{2}', nombre_TMDB)[0]    # filtramos por S01E01
    nombre_TMDB = re.split(r'[0-9]{2}[xX][0-9]{2}',nombre_TMDB)[0]
    nombre_TMDB = re.split(r'[0-9][xX][0-9]{2}', nombre_TMDB)[0]
    nombre_TMDB = re.split(r'Temporada', nombre_TMDB)[0]
    nombre_TMDB = re.split(r'HDTV', nombre_TMDB)[0]
    nombre_TMDB = re.split(r'Cap [0-9]{3}',nombre_TMDB)[0]
    nombre_TMDB = re.sub(r'\s+', '+', nombre_TMDB)    # Reemplazar espacios por '+'
    nombre_TMDB = re.sub(r'\++$', '', nombre_TMDB)    # Eliminar '+' al final
    
    return(nombre_TMDB)


def obtener_year(line):

    year_TMDB = re.findall(r'\d{4}(?=\.)|\d{4}(?=\))', line)
    print(year_TMDB)
    year_TMDB = year_TMDB[0] if year_TMDB else "NO"

    if year_TMDB in ["1080", "2160"]:
        return "NO"
    else:
        return year_TMDB



def info_tmdb(nombre_TMDB, year_TMDB, tipo):

    if tipo == "Serie":
        if year_TMDB == "NO":
            url = f"https://api.themoviedb.org/3/search/tv?api_key=2c0b5982e078e255ed5be3bba4c3064b&language=es&query={nombre_TMDB}"
        else:
            url = f"https://api.themoviedb.org/3/search/tv?api_key=2c0b5982e078e255ed5be3bba4c3064b&language=es&query={nombre_TMDB}&year={year_TMDB}"

        response = requests.get(url)
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            first_result = data['results'][0]  # Toma el primer resultado
            title = first_result.get('name', 'N/A')
            title = re.sub(r'\'', ' ', title)
            release_date = first_result.get('first_air_date', 'N/A')
            release_date = release_date.split("-")[0]
            original_title = first_result.get('original_name', 'N/A')
            id = first_result.get('id', 'N/A')
            log_monitor("Serie", f"{title} || {original_title}")
        else:
            # Manejar el caso donde no hay resultados
            log_monitor("IMDB", "No se encontraron resultados para la búsqueda")
            id,title,release_date,original_title = ('N/A', 'N/A', 'N/A', 'N/A')
            print(id)
            
        return (id, title, release_date, original_title)


    else:            #Pelicula
        if year_TMDB == "NO":
            url = f"https://api.themoviedb.org/3/search/movie?api_key=2c0b5982e078e255ed5be3bba4c3064b&query={nombre_TMDB}&language=es"
        else:
            url = f"https://api.themoviedb.org/3/search/movie?api_key=2c0b5982e078e255ed5be3bba4c3064b&query={nombre_TMDB}&year={year_TMDB}&language=es"

    response = requests.get(url)
    data = response.json()

    if 'results' in data and len(data['results']) > 0:
        first_result = data['results'][0]  # Toma el primer resultado
        title = first_result.get('title', 'N/A')
        release_date = first_result.get('release_date', 'N/A')
        release_date = release_date.split("-")[0]
        original_title = first_result.get('original_title', 'N/A')
        sinopsis = first_result.get('overview', 'N/A')
        id = first_result.get('id', 'N/A')
        log_monitor("Título Original", f"{title} || {original_title}")
        
    else:
        # Manejar el caso donde no hay resultados
        log_monitor("IMDB", "No se encontraron resultados para la búsqueda")
        id,title,release_date,original_title,sinopsis = ('N/A', 'N/A', 'N/A', 'N/A', 'N/A')

    return (id, title, release_date, original_title, sinopsis)


def episodios(line):

    episodio = re.sub(r'\.|\[|\]|\_|\(|\)|\+', ' ', line)  # quitamos caraceres raros
    patron1 = r"S([0-9]{2})E([0-9]{2})"      ### grupos de captura entre parentesis
    patron2 = r"([0-9]){1}[xX]([0-9]{2})"
    patron3 = r"([0-9]{2})[xX]([0-9]{2})"
    patron4 = r"Cap ([0-9])([0-9][0-9])"

    match = re.search(patron1, episodio) or re.search(patron2, episodio) or re.search(patron3, episodio) or re.search(patron4, episodio)
    resultado = match.group()
    season = match.group(1)
    season = str(season).zfill(2) # añade un 0 al inicio
    episode = match.group(2)
    episode = str(episode).zfill(2)
    log_monitor(resultado, f"Temporada: {season} || Episodio: {episode}")

    return(season,episode)



def info_tmdb_episodes(id,season,episode):


    url=f"https://api.themoviedb.org/3/tv/{id}/season/{season}/episode/{episode}?api_key=2c0b5982e078e255ed5be3bba4c3064b&language=es"
    response = requests.get(url)
    data = response.json()
    titulo_episodio = data.get('name', 'N/A')
    sinopsis= data.get('overview', 'N/A')
    log_monitor("Título", f"{titulo_episodio}")

    return (titulo_episodio,sinopsis)
    


def mediainfo(line):

    result = subprocess.run(["mediainfo", "--Output=JSON", line], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    media_info_json = json.loads(result.stdout)

    video_tracks = [track for track in media_info_json.get('media', {}).get('track', []) if track.get('@type') == 'Video']

    # Recorre cada track de video
    for video in video_tracks:
        extra = video.get('extra', 'N/A')  # Devuelve 'N/A' si 'extra' no está presente
        height = video.get('Height', 'N/A')  # Devuelve 'N/A' si 'height' no está presente

    return(extra,height)


def mediainfo_time(line):

    result = subprocess.run(["mediainfo", "--Output=JSON", line], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    media_info_json = json.loads(result.stdout)

    video_tracks = [track for track in media_info_json.get('media', {}).get('track', []) if track.get('@type') == 'General']

    # Recorre cada track de video
    for video in video_tracks:
        duration_seconds = video.get('Duration', 'N/A')  # Devuelve 'N/A' si 'extra' no está presente
        # Convertir la duración a un número flotante
        duration_seconds = float(duration_seconds)

        # Convertir a horas, minutos y segundos
        hours = int(duration_seconds // 3600)
        minutes = int((duration_seconds % 3600) // 60)
        seconds = int(duration_seconds % 60)

        # Mostrar duración en formato legible
        formatted_duration = f"{hours}:{minutes:02d}:{seconds:02d}"


    return(formatted_duration)



def pixels(line, extra, height):

    height = int(height)
                                                  # Verificamos si extra es un diccionario
    if isinstance(extra, dict):
        extra = extra.get('OriginalSourceMedium')
    else:
        extra = extra                              # Si es una cadena, asignamos el valor tal cual
    

    if height < 1080 or (height > 1080 and height < 2160):
        formato = "Rip"
    elif extra == 'Blu-ray' and height == 1080:
        formato = "Blu-ray" 
    elif extra == 'Blu-ray' and height == 2160:
        formato = "Ultra HD"
    else:
        formato = "Remux"

    return(formato)


def rename(line,title,release_date,formato,height,duration,monitor,titulo_episodio="N/A",season="N/A",episode="N/A"):

    height = int(height)
    if height == 2160:
        height = "4K"
    else:
        height =f"{height}p"

    parts = line.split("/")
    carpeta = "/".join(parts[:-1])
    ext = line[-4:]
    log_monitor("Carpeta",carpeta)
    if season == "N/A" and episode == "N/A":
        titulo_nuevo = f"{title} ({release_date}) {height} {formato}{ext}"
    else:
        titulo_nuevo = f"{title} ({release_date}) - S{season}E{episode} - {titulo_episodio} - {height} {formato}{ext}"

    if monitor == True:

        move = f'mv \"{line}\" \"Varios_Monitor/{titulo_nuevo}\"'
        print(move)
        subprocess.run(move, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log_monitor("Monitor || Fichero nuevo", f"Varios_Monitor/{titulo_nuevo} || {duration}")

    else:
        move = f'mv "{line}" "{carpeta}/{titulo_nuevo}"'
        print(move)
        subprocess.run(move, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log_monitor("Fichero nuevo", f"{carpeta}/{titulo_nuevo} || {duration}")
    

def limpieza(line):   # solo con monitor, desde Downloads


    line_modificado = line.split("/")[1]  # cogemos carpeta siguiente a Downloads
    deluge_info =f'deluge-console info 2>&1 | grep -v Deferred | grep "\[S\]" | grep -F "{line_modificado}"'
    output = subprocess.run(deluge_info, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    torrent = output.stdout.split()[-1]
    delete = f"deluge-console 'del -c --remove_data {torrent}'"
    subprocess.run(delete, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    log_monitor("limpieza Torrent", line_modificado)



def directorio_exp_2(nombre_film):

    mount = f"sudo mount /media/minipc/Expansion_2"
    subprocess.run(mount, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    directorio_nuevo = f'Expansion_2/Varios_Monitor/{nombre_film}'
    log_monitor("makemkvISO", directorio_nuevo)
    mkdir = f'mkdir -p \"{directorio_nuevo}\"'  
    subprocess.run(mkdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    return(directorio_nuevo)


def makemkvcon(directorio_nuevo,line):

    makemkv = f'makemkvcon mkv \"{line}\" all \"{directorio_nuevo}\"'
    print(makemkv)    
    subprocess.run(makemkv, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def rename_ficheros_tt(directorio,title,release_date):         

    busquedafind = f'find "{directorio}" -name "*t??.mkv"' 
    print(busquedafind)
    result = subprocess.run(busquedafind, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = result.stdout
    print(result)
    for line in result.splitlines():      # con salto de linea
        
        log_monitor("makemkvISO",line)
        ext = line[-6:]
        titulo_nuevo = f"{title} ({release_date})_{ext}"
        move = f"mv \"{line}\" \"{directorio}/{titulo_nuevo}\""
        print(move)
        subprocess.run(move, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        log_monitor("makemkvISO || Fichero nuevo", f"{directorio}/{titulo_nuevo}")


def convertir_pelicula_a_json(id, title, release_date, original_title, height, formato, sinopsis, duration, carpeta, hdd):
    height = int(height)
    if height == 2160:
        height = "4K"
    else:
        height = f"{height}p"

    pelicula_data = {
        "id TMDB": id,
        "Título": title,
        "Estreno": release_date,
        "Título Original": original_title,
        "Resolución": height,
        "Formato": formato,
        "Sinopsis": sinopsis,
        "Duración": duration,
        "Ubicación": carpeta,        
        "HDD": hdd
    }

    # Convertir el diccionario a JSON con codificación UTF-8
    pelicula_json = json.dumps(pelicula_data, indent=4, ensure_ascii=False)
    return pelicula_json


def convertir_episodio_a_json(id,title,release_date,original_title,height,formato,season,episode,titulo_episodio,sinopsis,duration,carpeta,hdd):

    height = int(height)
    if height == 2160:
        height = "4K"
    else:
        height = f"{height}p"

    episodio_data = {
        "id TMDB": id,
        "Título": title,
        "Estreno": release_date,
        "Título Original": original_title,
        "Resolución": height,
        "Formato": formato,
        "Temporada": season,
        "Episodio": episode,
        "Título Episodio": titulo_episodio,
        "Sinopsis": sinopsis,
        "Duración": duration,
        "Ubicación": carpeta,        
        "HDD": hdd
    }

    # Convertir el diccionario a JSON con codificación UTF-8
    episodio_json = json.dumps(episodio_data, indent=4, ensure_ascii=False)
    return episodio_json



def post_elastic(entrada_json,index,id):

    url = f"http://192.168.1.46:9200/{index}/_doc/"       ### con elementos duplicados
    #url = f"http://192.168.1.46:9200/{index}/_doc/{id}"  ### id unico
    headers = {"Content-Type": "application/json; charset=UTF-8"}  # Especificar la codificación UTF-8
    response = requests.post(url, headers=headers, data=entrada_json.encode('utf-8'))  # Codificar como UTF-8

    if response.status_code == 201:
        print("Documento añadido exitosamente:", response.json())
    else:
        print(f"Error al añadir documento. Código de estado: {response.status_code}")
        print("Detalles:", response.json())

