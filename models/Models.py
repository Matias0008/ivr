# Este archivo sirve como archivo en comun para generar los modelos en tablas de Postgres
from models.Base import base

from models.Estado import Estado
from models.Cliente import Cliente
from models.CambioEstado import CambioEstado
from models.Llamada import Llamada
from models.RespuestaPosible import RespuestaPosible
from models.RespuestasCliente import RespuestaDeCliente
from models.Encuesta import Encuesta
from models.Pregunta import Pregunta
