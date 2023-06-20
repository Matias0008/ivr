from sqlalchemy import  Column, Integer, String, func
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class RespuestaPosible(base):
    __tablename__ = "respuestaposible"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    respuestasDeCliente = relationship("RespuestaDeCliente", back_populates="respuestaPosible")

    def getDescripcion(self):
        return self.descripcion