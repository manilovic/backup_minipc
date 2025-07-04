#!/usr/bin/env python3

import time
import sys
import subprocess
import re
import argparse
from tools_python import log_monitor, create_lock, remove_lock, busqueda_serie, obtener_nombre_pelicula, obtener_nombre_serie, obtener_year, episodios, info_tmdb_episodes, info_tmdb, mediainfo,  mediainfo_time, pixels, rename, limpieza


create_lock("monitor")


try:
    
    parser = argparse.ArgumentParser(description='Script con argumentos -d y -m.')
    
    parser.add_argument('-d', '--directorio', type=str, help='Ruta del directorio', required=True)
    parser.add_argument('-m', '--modo', action='store_true', help='Monitor', required=False)
    
    args = parser.parse_args()
    
    directorio = args.directorio
    monitor = args.modo
    
    print("Script Monitor")
    print(f"Directorio: {args.directorio}")
    print(f"Monitor: {args.modo}")

    busquedafind = f'find "{directorio}" -type f -size +300M -mmin +1 \( -name "*.avi" -o -name "*.mkv" -o -name "*.mp4" \)'
    result = subprocess.run(busquedafind, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = result.stdout
    print(result)

    resultados = []

    ########
    

    for line in result.splitlines():      # con salto de linea

        log_monitor(" "," ")
        
        if busqueda_serie(line) == "Serie":
            tipo = "Serie"
            print(tipo)

            nombre = line.split("/")[-1]
            nombre_TMDB = obtener_nombre_serie(nombre)
            print(nombre_TMDB)
            year_TMDB = obtener_year(nombre)
            print(year_TMDB)

            season,episode = episodios(line)
            print(season,episode)


            id, title, release_date, original_title = info_tmdb(nombre_TMDB,year_TMDB,tipo)
            print(id, title, release_date, original_title)


            titulo_episodio = info_tmdb_episodes(id,season,episode)
            if title == "N/A":
                continue

            extra,height = mediainfo(line)
            print(extra,height)
            formato = pixels(line,extra,height)
            print(formato)
            duration = mediainfo_time(line)
            print(duration)

            rename(line,title,release_date,formato,height,monitor,titulo_episodio,season,episode)
            
            resultados.append(line)

            print("####")
            
        else:
            tipo = "Pelicula"
            print(tipo)

            nombre = line.split("/")[-1]
            nombre_TMDB = obtener_nombre_pelicula(nombre)
            year_TMDB = obtener_year(nombre)

            id, title, release_date, original_title = info_tmdb(nombre_TMDB,year_TMDB,tipo)
            print(id, title, release_date, original_title)
            if title == "N/A":
                continue

            extra,height = mediainfo(line)
            print(extra,height)

            duration = mediainfo_time(line)
            print(duration)

            formato = pixels(line,extra,height)
            print(formato)

            rename(line,title,release_date,formato,height,duration,monitor)

            resultados.append(line)
            
            print("####")

    #########


    if monitor == True:
        for registro in resultados:
            print(registro)
            limpieza(registro)
    

except Exception as e:
    print(f"Error: {e}")
finally:
    log_monitor("monitor","Script finalizado")
    remove_lock("monitor")
