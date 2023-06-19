import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.Cliente_model import Cliente
from models.Estado_model import Estado
from models.CambioEstado_model import CambioEstado
from models.Llamada_model import Llamada
from models.Base import base

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

    def createTables(self):
        base.metadata.create_all(self.engine)
    
    def conseguirClientes(self):
        self.connect()  # Conecta la sesión antes de usarla
        clientes = self.session.query(Cliente).all()
        return clientes
