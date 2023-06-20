from sqlalchemy import  Column, Integer, String,  ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class RespuestaDeCliente(base):
    __tablename__ = "respuestadecliente"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fechaEncuesta = Column(DateTime, default=func.now())
    descripcion = Column(String)
    respuestaPosibleId = Column(Integer, ForeignKey('respuestaposible.id'))
    respuestaPosible = relationship("RespuestaPosible", back_populates="respuestasDeCliente")
    llamadaId = Column(Integer, ForeignKey('llamada.id'))
    llamada = relationship("Llamada", back_populates="respuestasDeCliente")

    def getNombre(self):
        return self.nombre