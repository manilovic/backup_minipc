#!/usr/bin/env python3

import time
import sys
import subprocess
import re
import argparse
#monitor
from tools_python import log_monitor, create_lock, remove_lock, busqueda_serie, obtener_nombre_pelicula, obtener_nombre_serie, obtener_year, episodios, info_tmdb_episodes, info_tmdb, mediainfo,  mediainfo_time, pixels, rename, limpieza
#pp
from tools_python import convertir_pelicula_a_json, convertir_episodio_a_json, post_elastic


create_lock("registros")


try:

    # Configuración de argparse
    parser = argparse.ArgumentParser(description='Script <indice> con argumentos -d y -m.')

    parser.add_argument("indice", type=str, help="Nombre del índice de Elasticsearch.")  #required=True) no se necesita aqui, solo con --
    parser.add_argument('-d', '--directorio', type=str, help='Ruta del directorio', required=True)
    parser.add_argument('-m', '--modo', action='store_true', help='Monitor', required=False)
    

    args = parser.parse_args()
    
    directorio = args.directorio
    monitor = args.modo
    indice = args.indice
    
    print("Script Registros")
    print(f"Indice: {indice}")
    print(f"Directorio: {args.directorio}")
    print(f"Monitor: {args.modo}")

    busquedafind = f'find "{directorio}" -type f -size +50M -mmin +1 \( -name "*.avi" -o -name "*.mkv" -o -name "*.mp4" \)'
    result = subprocess.run(busquedafind, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = result.stdout
    print(result)


    ########
    

    for line in result.splitlines():      # con salto de linea

        log_monitor(" "," ")
        
        if busqueda_serie(line) == "Serie":
            tipo = "Serie"
            print(tipo)

            ## Expansion_2/Starwars_series/Obi-Wan\ Kenobi\ \(2022\)/Obi-Wan\ Kenobi\ \(2022\)\ -\ S01E01\ -\ Parte\ I\ \(1080p\).mkv 
            
            nombre = line.split("/")[-1]
            nombre_TMDB = re.split(r'\([0-9]{4}\)', nombre)[0] # filtramos por año (xxxx)
            year_TMDB = obtener_year(nombre)
            print(year_TMDB)

            season,episode = episodios(nombre)
            print(season,episode)

            carpeta= line.split("/")[1:-1]  ## selecciona todos los elementos de la lista excepto el primero ([0]) y el último ([-1]).

            hdd= line.split("/")[0]


            id, title, release_date, original_title = info_tmdb(nombre_TMDB,year_TMDB,tipo)
            print(id, title, release_date, original_title)


            titulo_episodio, sinopsis = info_tmdb_episodes(id,season,episode)
            if title == "N/A":
                continue
            
            print(titulo_episodio)
            print(sinopsis)

            extra,height = mediainfo(line)
            print(extra,height)
            formato = pixels(line,extra,height)
            print(formato)
            duration = mediainfo_time(line)
            print(duration)

            episodio_json = convertir_episodio_a_json(id,title,release_date,original_title,height,formato,season,episode,titulo_episodio,sinopsis,duration,carpeta,hdd)
            
            print(episodio_json)

            post_elastic(episodio_json,indice,id)
            

            #rename(line,title,release_date,formato,height,monitor,titulo_episodio,season,episode)
            
            #resultados.append(line)

            print("####")
            
        else:
            tipo = "Pelicula"
            print(tipo)

            ### 'Expansion_2/Starwars_films/Rogue One (2016) 2160p Blu-ray.mkv'

            nombre = line.split("/")[-1]
            nombre_TMDB = re.split(r'\([0-9]{4}\)', nombre)[0] # filtramos por año (xxxx)
            
            year_TMDB = obtener_year(nombre)

            carpeta= line.split("/")[1:-1]  ## selecciona todos los elementos de la lista excepto el primero ([0]) y el último ([-1]).

            hdd= line.split("/")[0]

            id, title, release_date, original_title, sinopsis = info_tmdb(nombre_TMDB,year_TMDB,tipo)
            print(id, title, release_date, original_title, sinopsis)
            if title == "N/A":
                continue

            extra,height = mediainfo(line)
            print(extra,height)

            duration = mediainfo_time(line)
            print(duration)

            formato = pixels(line,extra,height)
            print(formato)

            pelicula_json = convertir_pelicula_a_json(id,title,release_date,original_title,height,formato,sinopsis,duration,carpeta,hdd)
                
            print(pelicula_json)

            post_elastic(pelicula_json,indice,id)
            
            print("####")

    #########


    

except Exception as e:
    print(f"Error: {e}")
finally:
    log_monitor("registros","Script finalizado")
    remove_lock("registros")
