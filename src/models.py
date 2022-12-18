from sqlalchemy import Column, Integer, String
from load import Base

class Person(Base):
    __tablename__ = 'people' 
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Films(Base):
    __tablename__ = 'pelis'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Planeta(Base):
    __tablename__ = 'planetas'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Especie(Base):
    __tablename__ = 'especies'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    classification = Column(String)