from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

from models.Models import *

class Cliente(base):
    __tablename__ = "cliente"
    
    dni = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    nroCelular = Column(Integer)
    llamadas = relationship("Llamada", back_populates='cliente')

    def esCliente(self, dni: Integer):
        return self.dni == dni

    def getNombre(self):
        return f"{self.nombre} {self.apellido}"