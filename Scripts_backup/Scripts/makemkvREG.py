#!/usr/bin/env python3


import urllib.request
import subprocess
import sqlite3
from tools_python import log_monitor


headers = {'User-Agent': 'Mozilla/5.0'}
url = "https://forum.makemkv.com/forum/viewtopic.php?f=5&t=1053"

request = urllib.request.Request(url, headers=headers)  # Crear el objeto Request con la URL y los headers
response = urllib.request.urlopen(request)   # ORIGINAL # response = urllib.request.urlopen(url, headers=headers)
html = response.read().decode('utf-8')
    
x = "<code>"
start = html.find(x) +6 
y = "</code>"
end = html.find(y)
code= html[start:end]

registro = "makemkvcon reg " + code
subprocess.run(registro, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

log_monitor("makemkvREG", f"Código Insertado: {code}")
