from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

LlamadaBase = declarative_base()

class Llamada(LlamadaBase):
    __tablename__ = "llamada"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcionOperador = Column(String)
    detalleAccionRequerida = Column(String)
    duracion = Column(Integer)
    encuestaEnviada = Column(Boolean)
    observacionAuditor = Column(String)
    clienteId = Column(Integer, ForeignKey('cliente.id'))
    cliente = relationship("Cliente", back_populates="llamada")
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