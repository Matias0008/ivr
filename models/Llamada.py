from typing import List
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from design.IteradorCambioEstado import IteradorCambioEstado

from models.Base import base

class Llamada(base):
    __tablename__ = "llamada"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcionOperador = Column(String, nullable=True)
    detalleAccionRequerida = Column(String, nullable=True)
    duracion = Column(Integer)
    encuestaEnviada = Column(Boolean)
    observacionAuditor = Column(String, nullable=True)
    clienteDni = Column(Integer, ForeignKey('cliente.dni'))
    cliente = relationship("Cliente", back_populates="llamadas")
    cambiosEstado = relationship("CambioEstado", back_populates="llamada")
    respuestasDeCliente = relationship("RespuestaDeCliente", back_populates="llamada")

    def esDePeriodo(self, fechaInicio: String, fechaFin: String): #9
        fechaCreacion = self.determinarEstadoInicial()
        return fechaInicio <= fechaCreacion <= fechaFin

    def crearIterador(self):
        return IteradorCambioEstado(self.cambiosEstado)

    def determinarEstadoInicial(self): #10
        iterador = self.crearIterador()
        return iterador.primero().getFechaHoraInicio()
    
    def getDuracion(self): #24
        return self.duracion
    
    def tieneEncuestaRespondida(self): #12
        return len(self.respuestasDeCliente) > 0
    
    def getNombreClienteDeLlamadaYEstadoActual(self): # 18
        nombreCliente = self.cliente.getNombreCompleto()
        nombreUltimoEstado = self.determinarUltimoEstado() # Llama al 20
        return [nombreUltimoEstado, nombreCliente]

    def determinarUltimoEstado(self): # 20
        for cambioEstado in self.cambiosEstado:
            if cambioEstado.noTieneFechaHoraFin():
                # Aca ya tengo el ultimo cambio de estado
                return cambioEstado.getNombreEstado()
    
    def getRespuestas(self): #26
        descripciones = []
        for respuesta in self.respuestasDeCliente:
            descripciones.append(respuesta.getDescripcionRespuesta())
        return descripciones