from dotenv import load_dotenv

from controllers.GestorConsultarEncuesta import *
from controllers.Database import *

if __name__ == "__main__":
    load_dotenv()
    # database = DatabaseController()
    # database.createTables()

    encuestaGestor = GestorConsultarEncuesta()
    encuestaPantalla = PantallaConsultarEncuesta(encuestaGestor)
    encuestaGestor.setPantalla(encuestaPantalla)
    encuestaPantalla.tomarOpcionConsultarEncuesta()