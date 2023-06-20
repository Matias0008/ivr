import tkinter as tk

from views.encuesta_view import *
from controllers.db_controller import *
from models.Llamada_model import Llamada

class EncuestaController:
    pantalla: EncuestaBoundary
    fechaFin: str
    fechaInicio: str
    llamadasDentroDePeriodo: List[Llamada]

    def setPantalla(self, pantalla: EncuestaBoundary):
        self.pantalla = pantalla

    def consultarEncuesta(self):
        self.pantalla.habilitarFiltrosPorPeriodo()
    
    def tomarPeriodo(self, fechaInicio: str, fechaFin: str):
        self.fechaInicio = fechaInicio
        self.fechaFin = fechaFin 
        self.buscarLlamadasDentroDePeriodo(self.fechaInicio, self.fechaFin)

    def buscarLlamadasDentroDePeriodo(self, fechaInicio: str, fechaFin: str):
        db = DatabaseController()
        db.connect()
        llamadas: List[Llamada] = db.session.query(Llamada).all()
        for llamada in llamadas:
            if llamada.esDePeriodo(fechaInicio, fechaFin):
                self.llamadasDentroDePeriodo.append(llamada)
        self.pantalla.mostrarLlamadas([])