from sqlalchemy import  Column, Integer, String, func, DateTime
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base
from models.Llamada import Llamada

class Encuesta(base):
    __tablename__ = "encuesta"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    fechaVigencia = Column(DateTime)
    preguntas = relationship("Pregunta", back_populates="encuesta")

    def esEncuestaDeCliente(self, llamadaSeleccionada: Llamada): #29
        respuestasCliente = llamadaSeleccionada.getRespuestas()
        resultado = True

        for pregunta in self.preguntas:
            resultado = pregunta.esEncuestaDeCliente(respuestasCliente)
            if not resultado:
                return resultado

        return self

    def getDescripcionEncuesta(self):
        return self.descripcion

    def armarEncuesta(self):
        descripciones = []
        for pregunta in self.preguntas:
            descripciones.append(pregunta.getDescripcion())
        return descripciones