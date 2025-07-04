#!/bin/bash


# Borrar logs más antiguos de 3 días
sudo journalctl --vacuum-time=3d

# Reiniciar systemd-journald 
sudo systemctl restart systemd-journald

echo "$(date '+%a %d %b %Y %H:%M:%S') || limpiar_logs_journal || Limpieza ejecutada ||" >> /home/minipc/LogsJM/monitor.txt


