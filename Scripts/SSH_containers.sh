#!/bin/bash



############
echo "DOCKER NODE-RED"
############

CONTAINER_ID=$(docker ps -a | grep node-red | awk -F" " '{print $1}')

docker exec "$CONTAINER_ID" /bin/bash -c "
    echo 'Ejecutando comandos en el contenedor...';
    ssh-keyscan -H 192.168.1.48 >> ~/.ssh/known_hosts;
    ssh-keyscan -H 192.168.1.46 >> ~/.ssh/known_hosts;
    ssh-keyscan -H 192.168.1.35 >> ~/.ssh/known_hosts;    
    ssh-keygen -t rsa -b 4096 -f /usr/src/node-red/.ssh/id_ed25519 -N '';
    echo -e \"Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile=/dev/null\n\" > ~/.ssh/config;
    echo \"Creado fichero ssh config\";
    echo \"Clave pública generada:\";"

clave=$(docker exec "$CONTAINER_ID" /bin/bash -c "
    cat /usr/src/node-red/.ssh/id_ed25519.pub")

echo "$clave"

echo "$clave" >> ~/.ssh/authorized_keys                  # Clave a MINIPC 

ssh-keyscan -H 192.168.1.46 >> ~/.ssh/known_hosts        # desde MINIPC a Pi3#
sshpass -p "pi3" ssh -t pi3@192.168.1.46 << EOF
echo "$clave" >> ~/.ssh/authorized_keys
EOF

ssh-keyscan -H 192.168.1.35 >> ~/.ssh/known_hosts        # desde MINIPC a juan.gonzalez #
sshpass -p "lynx.2023" ssh -t juan.gonzalez@192.168.1.35 << EOF
echo "$clave" >> ~/.ssh/authorized_keys
EOF


echo "$(date '+%c') || SSH_containers || Node-Red hecho ||" >> LogsJM/updates_containers.txt


############
echo "HOMEASSISTANT"
###########

## Solo a PI3 ##

CONTAINER_ID=$(docker ps -a | grep homeassist | awk -F" " '{print $1}')

docker exec "$CONTAINER_ID" /bin/bash -c "
    echo 'Ejecutando comandos en el contenedor...';
    ssh-keyscan -H 192.168.1.46 >> ~/.ssh/known_hosts;   
    ssh-keygen -t rsa -b 4096 -f /root/.ssh/id_ed25519 -N '';
    echo -e \"Host *\n\tStrictHostKeyChecking no\n\tUserKnownHostsFile=/dev/null\n\" > ~/.ssh/config;
    echo \"Creado fichero ssh config\";
    echo \"Clave pública generada:\";"

clave=$(docker exec "$CONTAINER_ID" /bin/bash -c "
    cat /root/.ssh/id_ed25519.pub;")

echo "$clave"

echo "$clave" >> ~/.ssh/authorized_keys               # Clave a MINIPC

sshpass -p "pi3" ssh -t pi3@192.168.1.46 << EOF
echo "$clave" >> ~/.ssh/authorized_keys
EOF

echo "$(date '+%c') || SSH_containers || Homeassistant hecho ||" >> LogsJM/updates_containers.txt
