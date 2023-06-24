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

    def esEncuestaDeCliente(self, respuestasCliente): #30
        return self.tieneRespuestaPosible(respuestasCliente)

    def tieneRespuestaPosible(self, respuestasCliente): #31
        rtaPosibleDescripcion = [rtaPosible.getDescripcion() for rtaPosible in self.respuestasPosible]

        for rtaCliente in respuestasCliente:
            if rtaCliente in rtaPosibleDescripcion:
                return True
        return False

    def getDescripcion(self):
        return self.descripcion