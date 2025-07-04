#!/usr/bin/env python3


import requests
import re
import json
import sys
import argparse
from datetime import datetime, timedelta


#argumentos = sys.argv[1:]
#print(argumentos)
#argumentos = [arg.lower() for arg in argumentos]                             # Convertir los argumentos a minúsculas

parser = argparse.ArgumentParser(description='Script con argumentos y -d')
parser.add_argument('argumentos', nargs='*', help='Lista de argumentos')      # Permite múltiples argumentos sin flags
parser.add_argument('-d', '--dias', type=int, default=1, help='Número de días a examinar (por defecto 1)')


args = parser.parse_args()                                                    # Parsear los argumentos


argumentos_minuscula = [arg.lower() for arg in args.argumentos]               # Convertir los argumentos sin flags a minúsculas
print(f"Argumentos: {argumentos_minuscula}")
print(f"Número de días: {args.dias}")                                         # Usar el valor de días


current_date = datetime.now().date()


url = "https://www.movistarplus.es/programacion-tv/TVE"
response = requests.get(url)

canales = []

if response.status_code == 200:
    html = response.text
    
    pattern = r'<a href="https://www.movistarplus.es/programacion-tv/'   
    busqueda = re.finditer(pattern, html)

    for match in busqueda:
        start = match.start() +53                                              
        end = html.find('">', start)                                            
        resultado = html[start:end]
        if "class" not in resultado:                                         # Descarta resultados que contengan "class"
            canales.append(resultado)

result = []

for i in range(args.dias):
    
    for canal in canales:
        url = f"https://www.movistarplus.es/programacion-tv/{canal}/{current_date}"
        response = requests.get(url)
        #print(response.text)  # Ver el HTML completo de la respuesta
        
        pattern = r'<script type="application/ld\+json">(.*?)</script>'
        matches = re.findall(pattern, response.text, re.DOTALL)

        if matches:
            json_data = matches[1]                          # Extrae el JSON-LD como texto
            data = json.loads(json_data)                    # Carga el JSON como diccionario
            item_list = data.get("itemListElement", [])     # Accede a la lista de programación

            for item in item_list:
                if all(arg in item["item"]["name"].lower() for arg in argumentos_minuscula):   # Verificar si todos los argumentos están en "name"
                    program_name = item["item"].get("name")
                    start_time = item["item"].get("startDate")                                 # Fecha en formato ISO8601
                    start_time = datetime.fromisoformat(start_time)                            # Formatear al formato deseado
                    fecha_formateada = start_time.strftime("%Y-%m-%d %H:%M")
                    channel = item["item"]["publishedOn"].get("name")
                    resultado = f"{fecha_formateada} >> {program_name} >> {channel.strip()}"
                    result.append(resultado)
    current_date = current_date + timedelta(days=1)
    print(f"Date: {current_date}")
                               

# Ordenar los resultados filtrados
sorted_eventos = sorted(result)  # Ya que las fechas están formateadas en 'Año-Mes-Día', sorted() funciona bien


# Imprimir las líneas ordenadas
for evento in sorted_eventos:
    print(evento)
