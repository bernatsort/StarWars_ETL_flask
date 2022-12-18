from flask import Flask, render_template  
from extract import Extract
from transform import Transform 
from load import Load
from models import Person, Films, Planeta, Especie 
import plotly
import json

# creamos el objeto app como una instancia de la clase Flask importada del paquete flask
app = Flask(__name__)

# creamos las instancias de las clases Extract, Transform y Load
extract = Extract()
transform = Transform()
load = Load()

# APIs 
people_url = 'https://swapi.dev/api/people/'
planets_url = 'https://swapi.dev/api/planets/'
films_url = 'https://swapi.dev/api/films/'
species_url =  'https://swapi.dev/api/species/'
vehicles_url = 'https://swapi.dev/api/vehicles/'
starships_url = 'https://swapi.dev/api/starships/'

# Creamos las rutas
# índice con los enlaces
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# personajes 
@app.route('/personajes', methods=['GET'])
def people_name(): 
    """ 
    Renders the people page with a list of character names.
    Returns a Flask response object with the rendered HTML.
    """
    # get a list of character names from the API
    people_names = transform.values_list(people_url, 'name')
    # guardamos los nombres de los personajes en la base de datos
    load.save_data_to_db(people_names, Person, 'people.db')
    # render the people template with the character names
    return render_template('people.html', data=people_names)

# películas
@app.route('/pelis', methods=['GET'])
def films_title():
    films_title = transform.values_list(films_url, 'title')
    # guardamos los títulos de las pelis en la base de datos
    load.save_data_to_db(films_title, Films, 'pelis.db')
    return render_template('films.html', data=films_title)

# planetas
@app.route('/planetas', methods=['GET'])
def planets_name():
    planets_name = transform.values_list(planets_url, 'name')
    # guardamos los planetas en la base de datos
    load.save_data_to_db(planets_name, Planeta, 'planetas.db')
    return render_template('planets.html', data=planets_name)

# gráfico 10 planetas con mayor número de habitantes
@app.route('/plots', methods=['GET'])
def planets_population():
    planets = extract.extract_paginated_data(planets_url)
    # listas con el nombre y la población de los 10 planetas más poblados
    top_10_planet_names, top_10_planet_population = transform.top_n(planets, 'name', 'population', 0, 10)
    # creamos el barplot con plotly
    fig1 = transform.create_bar_chart(x = top_10_planet_names, y = top_10_planet_population,
                            title="Top 10 planetas con mayor número de habitantes",
                            xaxis_title="Planetas",
                            yaxis_title="Número de habitantes")                 
    # guardamos el plot en formato jpeg en el directorio de trabajo
    load.save_plot(fig1, 'plots/top_10_planetas_habitantes.jpeg', 'jpeg')
    # convertimos el barplot a JSON
    graph1JSON = json.dumps(fig1, cls = plotly.utils.PlotlyJSONEncoder)
    # renderizamos el HTML template con el barplot JSON 
    return render_template("plots.html", graph1JSON = graph1JSON)

# gráficos con las 10 naves espaciales más caras
@app.route('/starships', methods=['GET'])
def starships_price():
    starships = extract.extract_paginated_data(starships_url)
    # listas con el nombre y el precio 
    top_10_starship_names, top_10_starship_prices = transform.top_n(starships, 'name', 'cost_in_credits', 0, 10)
    top_10_starship_names_noDS, top_10_starship_prices_noDS = transform.top_n(starships, 'name', 'cost_in_credits', 1, 11)
    # creamos los barplots con plotly
    fig2 = transform.create_bar_chart(x = top_10_starship_names, y = top_10_starship_prices,
                            title="Top 10 naves espaciales más caras",
                            xaxis_title="Naves espaciales",
                            yaxis_title="Coste en créditos")
    fig3 = transform.create_bar_chart(x = top_10_starship_names_noDS, y = top_10_starship_prices_noDS,
                            title="Top 10 naves espaciales más caras sin contar la Estrella de la Muerte",
                            xaxis_title="Naves espaciales",
                            yaxis_title="Coste en créditos")
    # guardamos el plot en formato jpeg en el directorio de trabajo
    load.save_plot(fig2, 'plots/top_10_naves_caras.jpeg', 'jpeg')
    load.save_plot(fig3, 'plots/top_10_naves_caras_sinDS.jpeg', 'jpeg')
    # convertimos el barplot a JSON
    graph2JSON = json.dumps(fig2, cls = plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls = plotly.utils.PlotlyJSONEncoder)
    # renderizamos el HTML template con el barplot JSON 
    return render_template("starships_plot.html", graph2JSON = graph2JSON, graph3JSON = graph3JSON) 

# especies: nombre y clasificación
@app.route('/especies', methods=['GET'])
def species_classification():
    species = extract.extract_paginated_data(species_url)
    species_classif = transform.classify(species, 'name', 'classification')
    # guardamos las especies y su clasificación en la base de datos
    load.save_data_to_db(species_classif, Especie, 'especies.db')

    return render_template("species_table.html", data=species_classif)


# se ejecutará solo si este archivo se está ejecutando como el archivo que arranca la aplicación 
if __name__ == '__main__':
    # llamamos al método app.run() para iniciar la aplicación Flask y hacerla accesible en el host y puerto especificados
    app.run(host="0.0.0.0", port=4000, debug=True)


