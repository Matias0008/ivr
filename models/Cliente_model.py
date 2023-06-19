from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import declarative_base

ClienteBase = declarative_base()

class Cliente(ClienteBase):
    __tablename__ = "cliente"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    apellido = Column(String)
