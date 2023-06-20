import os
from typing import List

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.Cliente_model import Cliente
from models.Estado_model import Estado
from models.CambioEstado_model import CambioEstado
from models.Llamada_model import Llamada
from models.RespuestasCliente_model import RespuestaDeCliente
from models.RespuestaPosible_model import RespuestaPosible
from models.Encuesta_model import Encuesta
from models.Pregunta_model import Pregunta


from models.Models import base

class DatabaseController:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def connect(self):
        if not self.session:
            self.session = self.Session()

    def disconnect(self):
        if self.session:
            self.session.close()
            self.session = None
        if self.engine:
            self.engine.dispose()
            self.engine = None

    def execute_query(self, query):
        self.connect()  # Conecta la sesión antes de usarla
        query = text(query)
        result = self.session.execute(query).fetchall()
        return result
    
    def insertData(self):
        self.connect()
        base.metadata.drop_all(self.engine)
        self.createTables()
        self.session.add_all([
            Cliente(dni = 44741306 ,nombre='Matias', apellido = 'Delgado', nroCelular = '3534197321'),
            Cliente(dni = 45678912 ,nombre='Valentino', apellido = 'Lattanzi', nroCelular = '3535630896'),
            Cliente(dni = 44551156 ,nombre='Alejo', apellido = 'Giustinich', nroCelular = '3536789451'),
            Cliente(dni = 45789763 ,nombre='Nicolas', apellido = 'Antuña', nroCelular = '3535670983'),
            Cliente(dni = 35603215 ,nombre='Ignacio', apellido = 'Gonzalez', nroCelular = '3534771816'),
            Estado(nombre='Iniciada'),
            Estado(nombre='Finalizada'),
            Estado(nombre='Cancelada'),
            Estado(nombre='En curso'),
            Estado(nombre='Descartada'),
            Estado(nombre='Pendiente de escucha'),
            Estado(nombre='Correcta'),
            Estado(nombre='Con observacion'),
            CambioEstado(fechaHoraInicio='2023-05-25 12:12:36', fechaHoraFin='2023-05-25 12:13:36', estadoId = 1, llamadaId = 1),
            CambioEstado(fechaHoraInicio='2023-05-25 12:19:36', fechaHoraFin='2023-05-25 12:20:36', estadoId = 4, llamadaId = 1),
            CambioEstado(fechaHoraInicio='2023-05-25 12:19:36', fechaHoraFin='2023-05-25 12:20:36', estadoId = 2, llamadaId = 1),
            CambioEstado(fechaHoraInicio='2023-05-25 12:19:36', fechaHoraFin='2023-05-25 12:20:36', estadoId = 6, llamadaId = 1),
            CambioEstado(fechaHoraInicio='2023-05-25 12:19:36', fechaHoraFin='2023-05-25 12:20:36', estadoId = 7, llamadaId = 1),
            CambioEstado(fechaHoraInicio='2023-05-25 12:00:00', fechaHoraFin=None, estadoId = 1, llamadaId = 2),
            CambioEstado(fechaHoraInicio='2023-06-30 12:19:36', fechaHoraFin=None, estadoId = 1, llamadaId = 3),
            CambioEstado(fechaHoraInicio='2023-08-19 12:19:36', fechaHoraFin=None, estadoId = 1, llamadaId = 4),
            Llamada(duracion=60, descripcionOperador='Descripcion del operador 1', detalleAccionRequerida='Se cancela tarjeta por robo', encuestaEnviada=False, observacionAuditor='', clienteDni=44741306),
            Llamada(duracion=30, descripcionOperador='Descripcion del operador 2', detalleAccionRequerida='Se pausa tarjeta por extravío', encuestaEnviada=False, observacionAuditor='', clienteDni=35603215),
            Llamada(duracion=20, descripcionOperador='Descripcion del operador 3', detalleAccionRequerida='Se renueva la tarjeta por extravío', encuestaEnviada=True, observacionAuditor='', clienteDni=45789763),
            Llamada(duracion=15, descripcionOperador='Descripcion del operador 4', detalleAccionRequerida='Se registra la notificación de robo', encuestaEnviada=True, observacionAuditor='', clienteDni=44741306),
            Encuesta(descripcion = 'Atención al cliente', fechaVigencia = '2023-05-24 12:12:36'),
            Encuesta(descripcion = 'Servicio', fechaVigencia = '2023-03-21 20:31:41'),
            Encuesta(descripcion = 'Conformidad', fechaVigencia = '2023-03-21 20:31:41'),
            Pregunta(encuestaId=1, descripcion = '¿Se sintió conforme con su la atención ofrecida?'),
            Pregunta(encuestaId=2, descripcion = '¿Cumplió su objetivo en esta llamada?'),
            Pregunta(encuestaId=3, descripcion = '¿Del 1 al 5, cómo puntuaría a su ayudante?'),
            RespuestaPosible(preguntaId = 1, descripcion = 'Si'),
            RespuestaPosible(preguntaId = 1, descripcion = 'No'),
            RespuestaPosible(preguntaId = 1, descripcion = 'Tal vez'),
            RespuestaPosible(preguntaId = 2, descripcion = 'Si'),
            RespuestaPosible(preguntaId = 2, descripcion = 'No'),
            RespuestaPosible(preguntaId = 2, descripcion = 'Tal vez'),
            RespuestaPosible(preguntaId = 3, descripcion = '1'),
            RespuestaPosible(preguntaId = 3, descripcion = '2'),
            RespuestaPosible(preguntaId = 3, descripcion = '3'),
            RespuestaPosible(preguntaId = 3, descripcion = '4'),
            RespuestaPosible(preguntaId = 3, descripcion = '5'),
            RespuestaDeCliente(fechaEncuesta='2023-06-01', respuestaPosibleId = 2, llamadaId=1),
            RespuestaDeCliente(fechaEncuesta='2023-06-01', respuestaPosibleId = 10, llamadaId=4),
            RespuestaDeCliente(fechaEncuesta='2023-05-25', respuestaPosibleId = 4, llamadaId=2)
        ])
        self.session.commit()

    def createTables(self):
        base.metadata.create_all(self.engine)
    
    def conseguirClientes(self) -> List[Cliente]:
        self.connect()
        clientes = self.session.query(Cliente).all()
        return clientes

    def conseguirLlamadas(self) -> List[Llamada]:
        self.connect()
        llamadas = self.session.query(Llamada).all()
        return llamadas 