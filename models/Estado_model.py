from sqlalchemy import  Column, Integer, String,  ForeignKey
from sqlalchemy.orm import declarative_base, relationship

EstadoBase= declarative_base()

class Estado(EstadoBase):
    __tablename__ = "estado"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    descripcion = Column(String)
    llamada_id = Column(Integer, ForeignKey('llamadas.id'))
    cambiosEstado = relationship("CambioEstado", back_populates="estado")

    def getNombre(self):
        return self.nombre