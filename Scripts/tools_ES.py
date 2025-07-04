import subprocess
import json

###  sys.path.append('/media/minipc/HDD/Scripts')  añadirlo al path 
###  for directory in sys.path:
###     print(directory)


def eliminar_todos(indice):


    curl = f"""curl -X POST "http://192.168.1.46:9200/{indice}/_delete_by_query" -H 'Content-Type: application/json' -d'
{{
  "query": {{
    "match_all": {{}}
  }}
}}'"""

    result = subprocess.run(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def busqueda(indice,campo,clave):

    curl = f"""curl -X GET "http://192.168.1.46:9200/{indice}/_search?pretty" -H 'Content-Type: application/json' -d'
{{
  "size":100,
  "query": {{
    "match": {{
      "{campo}": "{clave}"
    }}
  }}
}}'"""


    result = subprocess.run(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #print(result.stdout)
    result_json = json.loads(result.stdout)
    #id = result_json['hits']['hits'][0]['_id'] if result_json['hits']['hits'] else 'N/A' 
    value = result_json['hits']['total']['value']
    print(f"Resultados: {value}")
    print()

    ids = [hit["_id"] for hit in result_json['hits']['hits']]  ## lo mismo:
    #ids=[]
    #for hit in result_json['hits']['hits']:
    #    id = hit["_id"]
    #    ids.append(id)
        
    return (ids)


def eliminar(indice, id):

    for id in id:
        print(id)
        curl = f'curl -X DELETE "http://192.168.1.46:9200/{indice}/_doc/{id}"'
        print(curl)
        result = subprocess.run(curl, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(result.stdout)


