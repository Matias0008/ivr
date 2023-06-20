from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Llamada(base):
    __tablename__ = "llamada"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcionOperador = Column(String)
    detalleAccionRequerida = Column(String)
    duracion = Column(Integer)
    encuestaEnviada = Column(Boolean)
    observacionAuditor = Column(String)
    clienteDni = Column(Integer, ForeignKey('cliente.dni'))
    cliente = relationship("Cliente", back_populates="llamadas")
    cambiosEstado = relationship("CambioEstado", back_populates="llamada")

    def esDePeriodo(self, fechaInicio: String, fechaFin: String):
        fechaCreacion = self.determinarEstadoInicial()
        return fechaInicio <= fechaCreacion <= fechaFin
    
    def determinarEstadoInicial(self):
        fechaHoraInicioMenor = None

        for cambioEstado in self.cambiosEstado:
            fechaHoraInicio = cambioEstado.getFechaHoraInicio()
            if fechaHoraInicioMenor is None or fechaHoraInicio < fechaHoraInicioMenor:
                fechaHoraInicioMenor = fechaHoraInicio

        return fechaHoraInicioMenor

    def getDuracion(self):
        return self.duracion