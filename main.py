from dotenv import load_dotenv

from controllers.encuesta_controller import *
from controllers.db_controller import *
from models.Estado_model import Estado

if __name__ == "__main__":
    load_dotenv()
    db = DatabaseController()
    db.connect()
    e1 = Estado(nombre = "Nombre", descripcion = "Descripcion", cambiosEstado = [])
    db.session.add(e1)
    db.session.commit()

    encuestaGestor = EncuestaController()
    encuestaPantalla = EncuestaBoundary(encuestaGestor)
    encuestaGestor.setPantalla(encuestaPantalla)
    encuestaPantalla.opcionConsultarEncuesta()