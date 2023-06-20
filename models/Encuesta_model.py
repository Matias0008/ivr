from sqlalchemy import  Column, Integer, String, func, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Encuesta(base):
    __tablename__ = "encuesta"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    fechaVigencia = Column(DateTime)
    preguntas = relationship("Pregunta", back_populates="encuesta")

    def esEncuestaDeCliente(self):
        for pregunta in self.preguntas:
            return pregunta.esEncuestaDeCliente()
        
    def getDescripcionEncuesta(self):
        return self.descripcion

    def armarEncuesta(self):
        descripciones = []
        for pregunta in self.preguntas:
           descripciones.append(pregunta.getDescripcion())
        return descripciones