# busquedaTV.py

import requests
import re
import json
from datetime import datetime, timedelta

def buscar_programas(palabras_clave, dias=1):
    """
    Busca programas de TV en Movistar Plus según palabras clave y días de búsqueda.
    
    :param palabras_clave: Lista de palabras clave en minúsculas.
    :param dias: Número de días a examinar desde hoy.
    :return: Lista de resultados encontrados.
    """
    current_date = datetime.now().date()
    url = "https://www.movistarplus.es/programacion-tv/TVE"
    response = requests.get(url)

    canales = []
    result = []

    if response.status_code == 200:
        html = response.text
        pattern = r'<a href="https://www.movistarplus.es/programacion-tv/'   
        busqueda = re.finditer(pattern, html)

        for match in busqueda:
            start = match.start() + 53
            end = html.find('">', start)
            resultado = html[start:end]
            if "class" not in resultado:
                canales.append(resultado)

    for i in range(dias):
        for canal in canales:
            url = f"https://www.movistarplus.es/programacion-tv/{canal}/{current_date}"
            response = requests.get(url)
            pattern = r'<script type="application/ld\+json">(.*?)</script>'
            matches = re.findall(pattern, response.text, re.DOTALL)

            if matches:
                try:
                    data = json.loads(matches[1])
                    item_list = data.get("itemListElement", [])
                    for item in item_list:
                        if all(arg in item["item"]["name"].lower() for arg in palabras_clave):
                            program_name = item["item"].get("name")
                            start_time = item["item"].get("startDate")
                            start_time = datetime.fromisoformat(start_time)
                            fecha_formateada = start_time.strftime("%Y-%m-%d %H:%M")
                            channel = item["item"]["publishedOn"].get("name")
                            resultado = f"{fecha_formateada} >> {program_name} >> {channel.strip()}"
                            result.append(resultado)
                except (json.JSONDecodeError, IndexError):
                    continue
        current_date = current_date + timedelta(days=1)

    return sorted(result)

