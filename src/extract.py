import requests
from typing import List, Dict

class Extract():
    # Función que extrae todos los datos de la API de Star Wars (SWAPI)
    def extract_paginated_data(self, url: str) -> List[Dict]: 
        # lista vacía para almacenar los datos
        all_data = []
        # hacemos peticiones a la API hasta que no haya más páginas con datos
        while url:
            # petición GET a la API para extraer los datos 
            response = requests.get(url)
            # parseamos los datos JSON
            data = response.json()
            # añadimos los datos de la página actual a la lista de todos los datos
            all_data.extend(data["results"])
            # url de la próxima página o None si no hay más páginas
            url = data["next"]
        # devolvemos una lista con los datos 
        return all_data



        