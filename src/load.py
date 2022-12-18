import plotly.io as pio
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pathlib

Base = declarative_base()

class Load():
    # Función que guarda gráficos en el formato deseado (jpeg, png, etc) en la carpeta deseada
    def save_plot(self, fig, file, format: str) -> None:
        # Convertimos el file a un objeto Path
        """
        Use pathlib.Path class to create a Path object from the file argument 
        and pass it to the pio.write_image() function. 
        This allows you to handle both string and path-like file paths in a 
        consistent and efficient way.
        """
        file = pathlib.Path(file)
        # guarda el plot en el formato deseado 
        pio.write_image(fig, file, format=format)


    def save_data_to_db(self, data, model, db_name: str) -> None:
        """
        This function creates a database engine and a Session object 
        for interacting with the database.
        However, instead of creating all the tables specified by Base.metadata, 
        it creates only a single table with the name of the model passed in 
        as an argument. This means that each time the function is called 
        with a different db_name and model, it will create a new table in the 
        corresponding database with the name of the model.
        """
        # set up the database
        engine = create_engine(f'sqlite:///db/{db_name}')
        # create a table in the database with the name of the database
        Base.metadata.create_all(engine, tables=[model.__table__])
        # create a session to interact with the database
        Session = sessionmaker(bind=engine)
        session = Session()

        # Save each data element to the database, using the with statement to manage the session:
        """
         The with statement creates a Session object by calling the session object, 
         and assigns it to the s variable. The code inside the with block can then use 
         the s variable to interact with the database. When the with block is exited, 
         the Session object is automatically closed, ensuring that the session is properly 
         cleaned up. This eliminates the need to explicitly close the session 
         at the end of the function.
        """        
        with session as s:
            """
            We first check if data is a list. 
            If it is, we loop through each element in the list and check if it is a dictionary. 
            If it is, we use the double star operator to unpack the dictionary 
            and pass the individual key-value pairs as arguments to the model() function. 
            If the element is not a dictionary, we simply pass it as an argument 
            to the model() function. 
            If data is not a list, we pass it directly to the model() function.
            """
            if isinstance(data, list):
                for elem in data:
                    if isinstance(elem, dict):
                        # unpack dictionaries with multiple fields using the double star operator (**)
                        p = model(**elem)
                        s.add(p)
                        s.commit()
                    else:
                        p = model(name=elem)
                        s.add(p)
                        s.commit()
       
        """
        The ** operator to unpack the values in the elem dictionary into keyword arguments 
        for the model class. This allows you to insert multiple columns of data into the 
        database in a single query.
        """






