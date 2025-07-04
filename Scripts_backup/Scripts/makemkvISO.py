#!/usr/bin/env python3

import sys
import subprocess
import re
import argparse
from tools_python import log_monitor,create_lock,remove_lock,directorio_exp_2,obtener_nombre_pelicula,obtener_year,info_tmdb,makemkvcon,rename_ficheros_tt,limpieza



create_lock("makemkvISO")

try:
    ## Argumentos    # Crea el parser
    parser = argparse.ArgumentParser(description='Script con argumentos -d y -m.')

    parser.add_argument('-d', '--directorio', type=str, help='Ruta del directorio', required=True)
    parser.add_argument('-m', '--modo', action='store_true', help='Monitor', required=False)
    args = parser.parse_args()
    
    directorio = args.directorio
    monitor = args.modo
    
    print("Script makemkvISO")
    print(f"Directorio: {args.directorio}")
    print(f"Monitor: {args.modo}")

    busquedafind = f'find "{directorio}" -name "*.iso" -o  -wholename "*BDMV/index.bdmv" -mmin +1' 
    result = subprocess.run(busquedafind, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = result.stdout
    print(result)

    resultados = []
    

    for line in result.splitlines():      # con salto de linea

#Downloads/El Hobbit 2 Version Extendida [FullBluRay 1080p][Castellano AC3 5.1-Ingles DTS 5.1+Subs][ES-EN]/THE_HOBBIT__THE_DESOLATION_OF_SMAUG_EXTENDED_EDITION.iso
#Downloads/Creed [FullBluRay 1080p][Castellano AC3 5.1-Ingles DTS 5.1+Subs][ES-EN]/BDMV/index.bdmv

        
        log_monitor("makemkvISO",line)

        if ".iso" in line:
            print("Es un iso")

            nombre_iso = line.split("/")[-2]
            directorio_nuevo = directorio_exp_2(nombre_iso)
            print(directorio_nuevo)

            nombre_TMDB = obtener_nombre_pelicula(nombre_iso)
            print(nombre_TMDB)

            year_TMDB = obtener_year(nombre_iso)
            print(year_TMDB)

        else:
            print("Es un index")
            
            nombre_index = line.split("/")[-3]
            directorio_nuevo = directorio_exp_2(nombre_index)
            print(directorio_nuevo)

            nombre_TMDB = obtener_nombre_pelicula(nombre_index)
            print(nombre_TMDB)

            year_TMDB = obtener_year(nombre_index)
            print(year_TMDB)


        makemkvcon(directorio_nuevo,line)

        resultados.append(line)
        
        print(resultados)

        tipo = "Pelicula"
        id, title, release_date, original_title = info_tmdb(nombre_TMDB,year_TMDB,tipo)
        print(id, title, release_date, original_title)
        if title == "N/A":
            continue
        print(title)
        rename_ficheros_tt(directorio_nuevo,title,release_date)


except Exception as e:
    print(f"Error: {e}")
finally:
    if monitor == True:
        for registro in resultados:
            print(registro)
            #limpieza(line)

    log_monitor("makemkvISO","Script finalizado")
    remove_lock("makemkvISO")
