#!/usr/bin/env python3

import subprocess
import json
import argparse
import sys

from tools_python import create_lock,remove_lock
from tools_ES import eliminar_todos,busqueda,eliminar



create_lock("removeES")


# Configuración de argparse
parser = argparse.ArgumentParser(description="Script para eliminar registros en un índice de Elasticsearch.")
parser.add_argument("nombre_indice", type=str, nargs="?", help="Nombre del índice en ElasticSearch.")
parser.add_argument("nombre_campo", type=str, nargs="?", help="Nombre del campo en ElasticSearch.")
parser.add_argument("valor_patron", type=str, nargs="?", help="Patrón de búsqueda para el campo.")
parser.add_argument('-r', '--remove-all', type=str, help='Borra todos los registros de un índice específico')

# Parseo de argumentos
args = parser.parse_args()

indice = args.remove_all


if args.remove_all:
    eliminar_todos(indice)
    print(f"Borrado total efectuado: {indice}")
    print()

elif args.nombre_indice and args.nombre_campo and args.valor_patron:
    print(f"Búsqueda en el índice: {args.nombre_indice}, campo: {args.nombre_campo}, patrón: {args.valor_patron}")

    indice = args.nombre_indice
    campo = args.nombre_campo
    patron = args.valor_patron

    print(f"Indice: {args.nombre_indice}")
    print(f"Campo: {args.nombre_campo}")
    print(f"Patrón: {args.valor_patron}")
    print()
    #ids = busqueda(indice, campo, patron)
    #eliminar(indice,ids)


else:
    parser.print_help()  # Muestra ayuda si no se cumplen las condiciones


remove_lock("removeES")
