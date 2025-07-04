#!/usr/bin/env python3

import requests
import json

url = "https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/horaria/28079" ## MADRID

querystring = {"api_key":"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqdWFubWFfZnJAaG90bWFpbC5jb20iLCJqdGkiOiJhMzlmZjBiZC1hYTQ0LTQ1ZjEtYWFmOC1jYzAxNDIwMWUxNjYiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTcyNDA3MjgzMywidXNlcklkIjoiYTM5ZmYwYmQtYWE0NC00NWYxLWFhZjgtY2MwMTQyMDFlMTY2Iiwicm9sZSI6IiJ9.7l5kb6RT_k5mQbtUiWDoAjL0s6nNuYgWs9Fm0B1xzQA"}

headers = {
    'cache-control': "no-cache"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
#print(response)
data = response.json()
#print(data)
titulo = data.get('datos', 'N/A')
#print(titulo)

response = requests.get(titulo)
data = response.json()


Cielo_dic = {}

tt = data[0]['prediccion']['dia']

for dia in tt:
    fecha = dia['fecha']
    fecha = fecha[:11]
    #print(fecha)

    for valores in dia['estadoCielo']:
        registro = (f"{fecha}{valores['periodo']}:00:00 - {valores['descripcion']}")
        #print(registro)
        fecha_hora, valor = registro.split(" - ")
        Cielo_dic[fecha_hora] = []
        Cielo_dic[fecha_hora].append(valor)

    
    for valores in dia['temperatura']:
        registro = (f"{fecha}{valores['periodo']}:00:00 - {valores['value']}ºC")
        #print(registro)
        fecha_hora, valor = registro.split(" - ")

        if fecha_hora not in Cielo_dic:
            Cielo_dic[fecha_hora] = []

        Cielo_dic[fecha_hora].append(valor)
    
    
    for valores in dia['precipitacion']:
        registro = (f"{fecha}{valores['periodo']}:00:00 - {valores['value']} mm")
        #print(registro)
        fecha_hora, valor = registro.split(" - ")

        if fecha_hora not in Cielo_dic:
            Cielo_dic[fecha_hora] = []

        Cielo_dic[fecha_hora].append(valor)


    for valores in dia['probPrecipitacion']:
        previo = (f"{fecha}{valores['periodo']}:00:00 - {valores['value']}%")
        hora_inicio = int(valores['periodo'][:2])       # Los primeros dos caracteres: '08'
        hora_fin = int(valores['periodo'][2:]) - 1      # Los últimos dos caracteres: '14'
        
        if "0208" in previo or "0814" in previo or "1420" in previo: # or "0208" in previo:
            for hora in range(hora_inicio, hora_fin + 1):
                hora_formateada = f"{hora:02d}"
                registro = (f"{fecha}{hora_formateada}:00:00 - {valores['value']}%")
                #print(registro)
                fecha_hora, valor = registro.split(" - ")

                if fecha_hora not in Cielo_dic:
                    Cielo_dic[fecha_hora] = []
                
                Cielo_dic[fecha_hora].append(valor)



#print(Cielo_dic)
                
for key, value in Cielo_dic.items():
    print(f"{key}: {value}")










