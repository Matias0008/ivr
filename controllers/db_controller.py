import os
from typing import List

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.Cliente_model import Cliente
from models.Estado_model import Estado
from models.CambioEstado_model import CambioEstado
from models.Llamada_model import Llamada
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
            Cliente(dni = 44741306 ,nombre='Matias', apellido = 'Delgado', nroCelular = '154197321'),
            Cliente(dni = 45678912 ,nombre='Valentino', apellido = 'Lattanzi', nroCelular = '3535630896'),
            Cliente(dni = 44741306 ,nombre='Alejo', apellido = 'Giustinich', nroCelular = '3536789451'),
            Cliente(dni = 44741306 ,nombre='Nicolas', apellido = 'Antuña', nroCelular = '3535670983'),
            Cliente(dni = 44741306 ,nombre='Ignacio', apellido = 'Gonzalez', nroCelular = '3534771816')
        ])

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