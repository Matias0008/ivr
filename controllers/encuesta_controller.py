from datetime import datetime
import tkinter as tk

from views.encuesta_view import *
from controllers.db_controller import *
from models.Llamada_model import Llamada

class EncuestaController:
    pantalla: EncuestaBoundary
    fechaFin: str
    fechaInicio: str
    llamadasDentroDePeriodo: List[Llamada] = []
    llamadaSeleccionada: Llamada = []

    def setPantalla(self, pantalla: EncuestaBoundary):
        self.pantalla = pantalla

    def consultarEncuesta(self):
        self.pantalla.habilitarFiltrosPorPeriodo()
    
    def tomarPeriodo(self, fechaInicio: str, fechaFin: str):
        self.fechaInicio = datetime.strptime(fechaInicio, "%d/%m/%Y")
        self.fechaFin = datetime.strptime(fechaFin, "%d/%m/%Y")
        self.buscarLlamadasDentroDePeriodo(self.fechaInicio, self.fechaFin)

    def buscarLlamadasDentroDePeriodo(self, fechaInicio: str, fechaFin: str):
        self.llamadasDentroDePeriodo = []
        db = DatabaseController()
        db.connect()
        llamadas: List[Llamada] = db.session.query(Llamada).all()

        # Conseguimos las llamas que esten dentro de un periodo
        for llamada in llamadas:
            if llamada.esDePeriodo(fechaInicio, fechaFin):
                self.llamadasDentroDePeriodo.append(llamada)

        # Si no encontramos ninguna llamada lanzamos un mensaje de error
        if (len(self.llamadasDentroDePeriodo) == 0):
            self.pantalla.mostrarMensajeError(message="No hay llamadas dentro del periodo", title="No hay llamadas")
        else:
            self.pantalla.mostrarLlamadas(self.llamadasDentroDePeriodo)

    def tomarLlamada(self, llamadas: list[Llamada], llamadaId):
        # Obtenemos la clase Llamada, ya que la seleccion solo nos brinda la id de la misma.
        for llamada in llamadas:
            if llamada.id == llamadaId:
                self.llamadaSeleccionada = llamada