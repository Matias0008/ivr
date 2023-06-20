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
