from sqlalchemy import  Column, Integer, String, func, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Encuesta(base):
    __tablename__ = "encuesta"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    fechaVigencia = Column(DateTime)
    preguntas = relationship("Pregunta", back_populates="encuesta")

    def esEncuestaDeCliente(self, llamadaSeleccionada):
        respuestasCliente = llamadaSeleccionada.getRespuestas()
        resultado = True

        # Debemos validar que para todas las preguntas exista una respuesta del cliente
        for pregunta in self.preguntas:
            resultado = pregunta.esEncuestaDeCliente(respuestasCliente)
            if not resultado:
                return resultado
        
        return resultado
        
    def getDescripcionEncuesta(self):
        return self.descripcion

    def armarEncuesta(self):
        descripciones = []
        for pregunta in self.preguntas:
           descripciones.append(pregunta.getDescripcion())
        return descripciones