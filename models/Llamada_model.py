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
        ultimoCambioEstado = self.cambiosEstado[-1]
        fechaHoraInicio = ultimoCambioEstado.getFechaHoraInicio()
        return fechaInicio <= fechaHoraInicio <= fechaFin
    
    def determinarEstadoInicial(self):
        primerCambioEstado = self.cambiosEstado[0]
        estadoInicial = primerCambioEstado.getNombreEstado()

    def getDuracion(self):
        return self.duracion