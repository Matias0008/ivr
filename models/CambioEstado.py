from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class CambioEstado(base):
    __tablename__ = "cambioestado"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    fechaHoraInicio = Column(DateTime, default=func.now())
    fechaHoraFin = Column(DateTime, nullable=True)
    estadoId = Column(Integer, ForeignKey('estado.id'))
    estado = relationship("Estado", back_populates="cambiosEstado")
    llamadaId = Column(Integer, ForeignKey('llamada.id'))
    llamada = relationship("Llamada", back_populates="cambiosEstado")

    def getFechaHoraInicio(self): #11
        return self.fechaHoraInicio

    def getNombreEstado(self): # 22
        return self.estado.getNombre()
    
    def noTieneFechaHoraFin(self): # 21
        # Si devuelve True entonces el atributo fechaHoraFin es nulo, o sea, no tiene fechaHoraFin (es el ultimo cambio de estado)
        return self.fechaHoraFin is None