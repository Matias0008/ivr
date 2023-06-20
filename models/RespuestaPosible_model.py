from sqlalchemy import  Column, Integer, String, func, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class RespuestaPosible(base):
    __tablename__ = "respuestaposible"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    respuestasDeCliente = relationship("RespuestaDeCliente", back_populates="respuestaPosible")
    preguntaId = Column(Integer, ForeignKey('pregunta.id'))
    pregunta = relationship("Pregunta", back_populates="respuestasPosible")

    def getDescripcion(self):
        return self.descripcion
    
    def getPregunta(self):
        return self.pregunta