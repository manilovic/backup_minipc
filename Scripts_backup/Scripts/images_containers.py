#!/usr/bin/env python3


import docker
import os
import subprocess
import time
from tools_python import log_updates


client = docker.from_env()

lista = client.containers.list(all=True)     #  [<Container: c32c3bc071>, <Container: 44bf2106dc>, <Container: 99fbd378cf>]

images_to_pull = []


log_updates("images_containers","Actualizando containers" )


for container in lista:
    # Verificar si el contenedor tiene alguna etiqueta de imagen
    if container.image.tags:
        # Obtener el primer tag de la lista
        image_name = container.image.tags[0]
        print(f"ID: {container.id}, Nombre: {container.name}, Estado: {container.status}, Imagen: {image_name}")
        images_to_pull.append(image_name)
    else:
        print(f"ID: {container.id}, Nombre: {container.name}, Estado: {container.status}, Imagen sin etiqueta")

# Continuar con la lógica de actualización de imágenes
print("Lista de imágenes a actualizar:")
print(images_to_pull)


for image in images_to_pull:
    if "latest" in image:
        print(f"Pulling image: {image}")
        client.images.pull(image)
        print(f"Image pulled: {image}")
    else:
        print(f"Skipping image: {image}")


log_updates("images_containers","Imagenes descargadas" )


for container in lista: 
    print (f"{container} to stop and remove")
    container.stop()
    container.remove()


#container_name = 'portainer'
#image_name = 'portainer/portainer-ce:latest'
#ports = {'8000/tcp': 8000, '9443/tcp': 9443}  # Mapeo de puertos
#volumes = {
#    '/var/run/docker.sock': {
#        'bind': '/var/run/docker.sock',
#        'mode': 'rw'  
#    },
#    'portainer_data': {
#        'bind': '/data',
#        'mode': 'rw' 
#    }
#}


#log_updates("images_containers",f"Iniciando el contenedor '{container_name}'")
#print(f"Iniciando el contenedor '{container_name}'")
#container = client.containers.run(
#        image=image_name,
#        name=container_name,
#        ports=ports,
#        volumes=volumes,
#        restart_policy={'Name': 'always'},
#        detach=True  # Ejecutar en segundo plano (modo "detached")
#    )



# List all dangling images (images not associated with any tags)
dangling_images = client.images.list(filters={"dangling": True})

# Print the list of dangling images (unused)
for image in dangling_images:
    print(f"Dangling Image ID: {image.id}, Tags: {image.tags}")
    client.images.remove(image.id)
    print(f"Image {image.id} removed successfully.")


log_updates("images_containers","Disposotivo 'minipc'")

command = "docker-compose -f docker-compose.yml up -d"
subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
log_updates("images_containers","Creado stack homeassistant_nodered")
