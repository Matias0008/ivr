import os
from datetime import datetime
import tkinter as tk

from views.encuesta_view import *
from controllers.db_controller import *
from models.Llamada_model import Llamada
from models.Encuesta_model import Encuesta

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
        try:
            self.fechaInicio = datetime.strptime(fechaInicio, "%d/%m/%Y")
            self.fechaFin = datetime.strptime(fechaFin, "%d/%m/%Y")
            if (self.fechaFin < self.fechaInicio):
                return self.pantalla.mostrarMensajeError(message="La fecha fin es menor que la fecha de inicio", title="Fecha fin incorrecta")
        except:
            return self.pantalla.mostrarMensajeError(message="El periodo ingreso es incorrecto", title="Periodo incorrecto")

        self.buscarLlamadasDentroDePeriodo(self.fechaInicio, self.fechaFin)

    def buscarLlamadasDentroDePeriodo(self, fechaInicio: str, fechaFin: str):
        self.llamadasDentroDePeriodo = []
        db = DatabaseController()
        db.connect()
        llamadas: List[Llamada] = db.session.query(Llamada).all()

        # Conseguimos las llamas que esten dentro de un periodo
        for llamada in llamadas:
            if llamada.esDePeriodo(fechaInicio, fechaFin) and llamada.tieneEncuestaRespondida():
                self.llamadasDentroDePeriodo.append(llamada)

        # Si no encontramos ninguna llamada lanzamos un mensaje de error
        if (len(self.llamadasDentroDePeriodo) == 0):
            self.pantalla.mostrarMensajeError(message="No hay llamadas dentro del periodo", title="No hay llamadas")
        else:
            self.pantalla.mostrarLlamadas(self.llamadasDentroDePeriodo)

    def tomarLlamada(self, llamadaSeleccionada: Llamada):
        self.llamadaSeleccionada = llamadaSeleccionada
        self.obtenerDatosLlamada()

    def obtenerDatosLlamada(self):
        estadoActual, nombreCliente = self.llamadaSeleccionada.getNombreClienteDeLlamadaYEstadoActual()
        duracion = self.llamadaSeleccionada.getDuracion()
        descripcionEncuesta, descripcionPreguntas, descripcionRespuestas = self.obtenerDatosEncuesta()
        self.mostrarEncuestas(estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas)
    
    def obtenerDatosEncuesta(self):
        descripcionRespuestas = self.llamadaSeleccionada.getRespuestas()

        # Me conecto a la base de datos para obtener todas las encuestas
        db = DatabaseController()
        db.connect()

        encuestaCliente = []
        encuestas = db.session.query(Encuesta).all()
        for encuesta in encuestas:
            if encuesta.esEncuestaDeCliente():
                encuestaCliente = encuesta

        descripcionEncuesta = encuestaCliente.getDescripcionEncuesta()
        descripcionPreguntas = encuestaCliente.armarEncuesta()
        return [descripcionEncuesta, descripcionPreguntas, descripcionRespuestas]
    
    def mostrarEncuestas(self, estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas):
        self.pantalla.mostrarEncuestas(estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas)
    
    def generarCSV(self,estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas):
        print(estadoActual)
        with open('views/view.csv', 'w', encoding="UTF-8") as fp:
            contenido = f"""Nombre del cliente, Estado, Duracion\n{nombreCliente}, {estadoActual}, {duracion}\n"""

            for x, pregunta in enumerate(descripcionPreguntas):
                for y, respuesta in enumerate(descripcionRespuestas):
                    contenido += f"Pregunta: {x + 1}: {pregunta}, Respuesta: {y + 1}: {respuesta}\n"

            fp.write(contenido)
            pass