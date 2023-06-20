from sqlalchemy import  Column, Integer, String, func, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Encuesta(base):
    __tablename__ = "encuesta"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String)
    fechaVigencia = Column(DateTime)
    preguntas = relationship("Pregunta", back_populates="encuesta")
