from dotenv import load_dotenv

from controllers.encuesta_controller import *
from controllers.db_controller import *

if __name__ == "__main__":
    load_dotenv()
    encuestaGestor = EncuestaController()
    encuestaPantalla = EncuestaBoundary(encuestaGestor)
    encuestaGestor.setPantalla(encuestaPantalla)
    encuestaPantalla.opcionConsultarEncuesta()