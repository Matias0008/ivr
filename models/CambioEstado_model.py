from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

from models.Models import *

class CambioEstado(base):
    __tablename__ = "cambioestado"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fechaHoraInicio = Column(DateTime, default=func.now())
    fechaHoraFin = Column(DateTime)
    estadoId = Column(Integer, ForeignKey('estado.id'))
    estado = relationship("Estado", back_populates="cambioestado")
    llamadaId = Column(Integer, ForeignKey('llamada.id'))
    llamada = relationship("Llamada", back_populates="cambioestado")

    def getFechaHoraInicio(self):
        return self.fechaHoraInicio

    def getNombreEstado(self):
        return self.estado.nombre