import tkinter as tk

from views.encuesta_view import *

class EncuestaController:
    pantalla: EncuestaBoundary

    def setPantalla(self, pantalla: EncuestaBoundary):
        self.pantalla = pantalla

    def consultarEncuesta(self):
        self.pantalla.habilitarFiltrosPorPeriodo()