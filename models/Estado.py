from sqlalchemy import  Column, Integer, String,  ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Estado(base):
    __tablename__ = "estado"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String, nullable=True)
    cambiosEstado = relationship("CambioEstado", back_populates="estado")

    def getNombre(self):
        return self.nombre