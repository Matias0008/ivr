from sqlalchemy import  Column, Integer, String,  ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Pregunta(base):
    __tablename__ = "pregunta"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String, nullable=True)
    respuestasPosible = relationship("RespuestaPosible", back_populates="pregunta")
    encuestaId = Column(Integer, ForeignKey("encuesta.id"))
    encuesta = relationship("Encuesta", back_populates="preguntas")

    def esEncuestaDeCliente(self, respuestasCliente):
        return self.tieneRespuestaPosible(respuestasCliente)

    def tieneRespuestaPosible(self, respuestasCliente):
        # Lo que hacemos en esta funcion es validar si al menos una respuesta del cliente esta en nuestras respuestas posibles de la pregunta

        for respuesta in respuestasCliente:
            for respuestaPosible in self.respuestasPosible:
                if respuesta == respuestaPosible.getDescripcion():
                    return True
            return False
    
    def getDescripcion(self):
        return self.descripcion