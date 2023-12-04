from dotenv import load_dotenv

from controllers.GestorConsultarEncuesta import *
from controllers.Database import *

if __name__ == "__main__":
    load_dotenv()
    database = DatabaseController()
    database.insertData()
    # database = DatabaseController()
    # database.insertData()

    encuestaGestor = GestorConsultarEncuesta()
    encuestaPantalla = PantallaConsultarEncuesta(encuestaGestor)
    encuestaGestor.setPantalla(encuestaPantalla)
    encuestaPantalla.tomarOpcionConsultarEncuesta()