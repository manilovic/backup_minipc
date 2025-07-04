#!/bin/bash



# Verificar si se proporcionó al menos un argumento
if [ $# -eq 0 ]; then
    echo "Error: No se proporcionó ningún argumento."
    echo "Uso: $0 < pi3 o minipc >"
    exit 1
fi


# Variables

if [ "$1" = "pi3" ]
    then
       maquina="pi3"
fi
       
if [ "$1" = "minipc" ]
    then
       maquina="minipc"      
fi     


sudo rsync -a --delete docker 1-docker_"$maquina"


cd 1-docker_"$maquina"/

git config --global user.email "juanma_fr@hotmail.com"
git config --global user.name "manilovic"


sudo git add .
sudo git commit -m "Commit $(date)"



GIT_SSH_COMMAND="ssh -i /home/$maquina/.ssh/git -o StrictHostKeyChecking=no" git push --force origin master   ### Forzar si se ha tocado la nube

echo "$(date '+%c') || git_update_docker || Backup docker $maquina hecho ||" >> /home/minipc/LogsJM/monitor.txt

