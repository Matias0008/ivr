from sqlalchemy import  Column, Integer, String, BigInteger
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Cliente(base):
    __tablename__ = "cliente"
    
    dni = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    nroCelular = Column(BigInteger)
    llamadas = relationship("Llamada", back_populates='cliente')

    def getNombreCompleto(self): # 20
        return f"{self.nombre} {self.apellido}"