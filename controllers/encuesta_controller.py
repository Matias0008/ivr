import tkinter as tk

from views.encuesta_view import *

class EncuestaController:
    pantalla: EncuestaBoundary

    def consultarEncuesta(self):
        self.pantalla.habilitarFiltrosPorPeriodo()
    
    def setPantalla(self, pantalla: EncuestaBoundary):
        self.pantalla = pantalla