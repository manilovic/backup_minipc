#!/bin/bash


echo "$(date '+%Y-%m-%d %H:%M:%S') 'Empezando...Paso 1/2'" >> /home/minipc/log.txt


# Actualizando containers
if ./Scripts/images_containers.py >> /home/minipc/log.txt 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') 'Paso 1/2 completado correctamente.'" >> /home/minipc/log.txt
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') 'Error en Paso 1/2. Abortando.'" >> /home/minipc/log.txt
    exit 1
fi



echo "$(date '+%Y-%m-%d %H:%M:%S') 'Paso 2/2...'" >> /home/minipc/log.txt
sleep 1m 


echo "$(date '+%Y-%m-%d %H:%M:%S') 'Paso 3/2...'" >> /home/minipc/log.txt


# Ejecutar accesos SSH con manejo de errores
if ./Scripts/SSH_containers.sh >> /home/minipc/log.txt 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') 'Accesos SSH ejecutados correctamente.'" >> /home/minipc/log.txt
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') 'Error ejecutando SSH_containers.sh.'" >> /home/minipc/log.txt
    exit 1
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') 'Terminado'" >> /home/minipc/log.txt
