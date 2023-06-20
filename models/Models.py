# Este archivo sirve como archivo en comun para generar los modelos en tablas de Postgres
from models.Base import base

from models.Estado_model import Estado
from models.Cliente_model import Cliente
from models.CambioEstado_model import CambioEstado
from models.Llamada_model import Llamada
from models.RespuestaPosible_model import RespuestaPosible
from models.RespuestasCliente_model import RespuestaDeCliente
from models.Encuesta_model import Encuesta
from models.Pregunta_model import Pregunta
