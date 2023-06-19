import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from models.Cliente_model import Cliente
from models.Base import base

def check_database_connection(func):
    def wrapper(self, *args, **kwargs):
        if not self.engine or not self.Session:
            raise ConnectionError("La base de datos no está conectada")
        return func(self, *args, **kwargs)
    return wrapper

class DatabaseController:
    def __init__(self):
        self.db_url = os.environ.get('DATABASE_URL')
        self.engine = None
        self.Session = None
    
    @property
    def session(self):
        return self.Session

    def connect(self):
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def disconnect(self):
        if self.engine:
            self.engine.dispose()
        self.engine = None
        self.Session = None

    @check_database_connection
    def execute_query(self, query):
        session = self.Session()
        query = text(query)
        result = session.execute(query).fetchall()
        session.close()
        return result

    def createTables(self):
        base.metadata.create_all(self.engine)

    @check_database_connection
    def conseguirClientes(self):
        clientes = self.Session().query(Cliente).all()
        self.disconnect()
        return clientes