from sqlalchemy import  Column, Integer, String,  ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from models.Models import *

class Estado(base):
    __tablename__ = "estado"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    cambiosEstado = relationship("CambioEstado", back_populates="estado")

    def getNombre(self):
        return self.nombre