#!/bin/bash


# Verificar si se proporcionó al menos un argumento
if [ $# -eq 0 ]; then
    echo "Error: No se proporcionó ningún argumento."
    echo "Uso: $0 < start, stop, restart, reload, enale, disable, status >"
    exit 1
fi

#start	Inicia un servicio.
#stop	Detiene un servicio.
#restart	Reinicia un servicio.
#reload	Recarga la configuración del servicio.
#enable	Activa el inicio automático.
#disable	Desactiva el inicio automático.
#status	Muestra el estado del servicio.


if [ $1 == status ]
	then
	       systemctl status deluge*
	       exit 0
fi

echo "mini" | sudo -S systemctl $1 deluged
echo "mini" | sudo -S systemctl $1 deluge-web
