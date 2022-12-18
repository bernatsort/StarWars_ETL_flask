import plotly.express as px
from typing import List, Dict, Tuple, Any, Type
from extract import Extract

# creamos la instancia de la clase Extract
extract = Extract()

class Transform():
    # Función que guarda todos los values de una key específica en una lista
    def values_list(self, url: str, key: str) -> List[Any]:
        # guardamos los datos del diccionario que queramos en data
        data = extract.extract_paginated_data(url)
        # Extraemos todos los values y los guardamos en una lista
        values_list = []
        for values in data:
            values_list.append(values[key])
        return values_list

    # Función que genera una tupla con dos listas con los top n elementos 
    def top_n(self, my_list: List[Dict], key_1: str, key_2: str, n: int, m: int) -> Tuple[List[Any], List[int]]:
        # lista con el nombre de todos los elementos en la lista elem_1
        elem_1 = [elem[key_1] for elem in my_list]
        # lista con los key_2
        # si el value es 'unknown' lo sustituimos por 0
        elem_2_str = [elem[key_2] if elem[key_2] != 'unknown' else 0 for elem in my_list]
        # convertimos de str a int
        elem_2_int = list(map(int, elem_2_str))
        # ordenamos las listas en orden descendente
        elem_1 = [x for _, x in sorted(zip(elem_2_int, elem_1), reverse=True)]
        elem_2_int = sorted(elem_2_int, reverse=True)
        # top n elementos
        top_n_elem_1 = elem_1[n:m]
        top_n_elem_2 = elem_2_int[n:m]
        return top_n_elem_1, top_n_elem_2

    """
    Función itera sobre los elementos de la lista de datos y, para cada elemento, 
    crea un objeto que contiene los valores de los campos key_1 y key_2 del elemento. 
    Por ejemplo, si key_1 es "nombre" y key_2 es "clasificación", la función creará 
    un objeto que contendrá los campos nombre y clasificación del elemento.
    A continuación, la función añade cada objeto a la lista classif y, 
    por último, devuelve la lista classif.
    """
    def classify(self, data: List[Dict], key_1: str, key_2: str) -> List[Dict]:
        classif = []
        for elem in data:
            classif.append({
                key_1: elem[key_1],
                key_2: elem[key_2]
            })
        return classif

    """
    Función llamada create_bar_chart() que toma cinco argumentos: 
    x, y, title, xaxis_title, y yaxis_title. 
    La función crea un gráfico de barras utilizando plotly express, establece 
    el título y los títulos de los ejes, y devuelve el objeto figura resultante.
    """
    def create_bar_chart(self, x: List[Any], y: List[Any], title: str, xaxis_title: str, yaxis_title: str):
        fig = px.bar(x=x, y=y, title=title)
        fig.update_xaxes(title=xaxis_title)
        fig.update_yaxes(title=yaxis_title)
        return fig




