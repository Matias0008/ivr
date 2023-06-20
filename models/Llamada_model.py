from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

from models.Base import base

class Llamada(base):
    __tablename__ = "llamada"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcionOperador = Column(String, nullable=True)
    detalleAccionRequerida = Column(String, nullable=True)
    duracion = Column(Integer)
    encuestaRespondida = Column(Boolean)
    observacionAuditor = Column(String, nullable=True)
    clienteDni = Column(Integer, ForeignKey('cliente.dni'))
    cliente = relationship("Cliente", back_populates="llamadas")
    cambiosEstado = relationship("CambioEstado", back_populates="llamada")
    respuestasDeCliente = relationship("RespuestaDeCliente", back_populates="llamada")

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
    
    def tieneEncuestaRespondida(self):
        return self.encuestaRespondida
    
    def getNombreClienteDeLlamadaYEstadoActual(self): # 19
        nombreCliente = self.cliente.getNombreCompleto() # Llama al 20
        nombreUltimoEstado = self.determinarUltimoEstado() # Llama al 21
        return [nombreUltimoEstado, nombreCliente]

    def determinarUltimoEstado(self): # 21
        for cambioEstado in self.cambiosEstado:
            if cambioEstado.noTieneFechaHoraFin(): # Llama al 22
                # Aca ya tengo el ultimo cambio de estado
                return cambioEstado.getNombreEstado() # Llama al 24
    
    def getRespuestas(self):
        descripcionesRespuesta = []
        for respuesta in self.respuestasDeCliente:
            descripcionesRespuesta.append(respuesta.getDescripcionRespuesta())
        return descripcionesRespuesta