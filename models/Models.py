# Este archivo sirve como archivo en comun para generar los modelos en tablas de Postgres
from sqlalchemy.orm import declarative_base
base = declarative_base()

from models.Estado_model import Estado
from models.Cliente_model import Cliente
from models.CambioEstado_model import CambioEstado
from models.Llamada_model import Llamada