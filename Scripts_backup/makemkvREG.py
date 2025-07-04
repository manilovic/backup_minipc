#!/usr/bin/env python3


import urllib.request
import subprocess
import sqlite3
import re
from tools_python import log_monitor
from pathlib import Path



headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://forum.makemkv.com/forum/viewtopic.php?f=5&t=1053"

request = urllib.request.Request(url, headers=headers)  # Crear el objeto Request con la URL y los headers
response = urllib.request.urlopen(request)   # ORIGINAL # response = urllib.request.urlopen(url, headers=headers)
html = response.read().decode('utf-8')
    
#x = "<code>"
#start = html.find(x) +6 
#y = "</code>"
#end = html.find(y)
#code= html[start:end]



matches = re.findall(r"<code>(T-[A-Za-z0-9]+)</code>", html)
print(matches)  # ['T-abc123', 'T-def456']
code = matches[0]


# Ruta del archivo de configuración
ruta_config = Path.home() / ".MakeMKV" / "settings.conf"
print(ruta_config)

# Contenido deseado
nuevo_contenido = f"""#
# MakeMKV settings file, written by MakeMKV v1.17.9 linux(x64-release)
#
app_Key = "{code}"
sdf_Stop = ""
"""


# Escribir archivo
with open(ruta_config, "w") as f:
    f.write(nuevo_contenido)

print(f"Archivo sobrescrito en: {ruta_config}")

log_monitor("makemkvREG", f"Código Insertado: {code}")
