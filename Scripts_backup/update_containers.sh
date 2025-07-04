#!/bin/bash



# Actualizando containers
if ./Scripts/images_containers.py ; then
    echo "$(date '+%a %d %b %Y %H:%M:%S') || update_containers || Script iniciado ||" >> /home/minipc/LogsJM/monitor.txt
else 
    echo "$(date '+%a %d %b %Y %H:%M:%S') || update_containers || Error en Paso 1/2. Abortando ||" >> /home/minipc/LogsJM/monitor.txt  
    exit 1
fi


sleep 1m 



# Ejecutar accesos SSH con manejo de errores
if ./Scripts/SSH_containers.sh ; then
    #echo "$(date '+%Y-%m-%d %H:%M:%S') || update_containers || Accesos SSH ejecutados correctamente ||" >> /home/minipc/LogsJM/monitor.txt
    sleep 5s
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') || update_containers || Error ejecutando SSH_containers.sh ||" >> /home/minipc/LogsJM/monitor.txt
    exit 1
fi


docker images -f "dangling=true" -q | xargs docker rmi  ## -q lista solo el id

echo "$(date '+%a %d %b %Y %H:%M:%S') || update_containers || Script terminado ||" >> /home/minipc/LogsJM/monitor.txt

