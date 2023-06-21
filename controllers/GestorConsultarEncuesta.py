from datetime import datetime
import tkinter as tk

from views.PantallaConsultarEncuesta import *
from controllers.Database import *

from models.Llamada import Llamada
from models.Encuesta import Encuesta

class GestorConsultarEncuesta:
    pantalla: PantallaConsultarEncuesta
    fechaFin: str
    fechaInicio: str
    llamadasDentroDePeriodo: List[Llamada] = []
    llamadaSeleccionada: Llamada = []

    def setPantalla(self, pantalla: PantallaConsultarEncuesta):
        self.pantalla = pantalla

    def consultarEncuesta(self):
        self.pantalla.habilitarFiltrosPorPeriodo()
    
    def tomarPeriodo(self, fechaInicio: str, fechaFin: str):
        try:
            self.fechaInicio = datetime.strptime(fechaInicio, "%d/%m/%Y")
            self.fechaFin = datetime.strptime(fechaFin, "%d/%m/%Y")

            # Validacion extra para que no se pueda insertar una fecha fin mayor que la de inicio
            if (self.fechaFin < self.fechaInicio):
                return self.pantalla.mostrarMensajeError(parent=self.pantalla.filtrosFrame,message="La fecha de fin es menor que la fecha de inicio", title="Fecha  de fin incorrecta")
        except:
            return self.pantalla.mostrarMensajeError(parent=self.pantalla.filtrosFrame,message="El periodo ingreso es incorrecto", title="Periodo incorrecto")

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
            return self.pantalla.mostrarMensajeError(parent=self.pantalla.filtrosFrame,message="No hay llamadas dentro del periodo", title="No hay llamadas")
        
        self.pantalla.mostrarLlamadas(self.llamadasDentroDePeriodo)

    def tomarLlamada(self, llamadaSeleccionada: Llamada):
        self.llamadaSeleccionada = llamadaSeleccionada
        self.obtenerDatosLlamada()

    def obtenerDatosLlamada(self):
        # Primero obtenemos los datos de la llamada
        estadoActual, nombreCliente = self.llamadaSeleccionada.getNombreClienteDeLlamadaYEstadoActual()
        duracion = self.llamadaSeleccionada.getDuracion()

        # Luego obtenemos los datos de la encuesta
        descripcionEncuesta, descripcionPreguntas, descripcionRespuestas = self.obtenerDatosEncuesta()
        self.mostrarEncuesta(estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas)
    
    def obtenerDatosEncuesta(self):
        descripcionRespuestas = self.llamadaSeleccionada.getRespuestas()

        # Me conecto a la base de datos para obtener todas las encuestas
        db = DatabaseController()
        db.connect()
        encuestaCliente = []
        encuestas = db.session.query(Encuesta).all()

        for encuesta in encuestas:
            if encuesta.esEncuestaDeCliente(self.llamadaSeleccionada):
                encuestaCliente = encuesta

        descripcionEncuesta = encuestaCliente.getDescripcionEncuesta()
        descripcionPreguntas = encuestaCliente.armarEncuesta()
        return [descripcionEncuesta, descripcionPreguntas, descripcionRespuestas]
    
    def mostrarEncuesta(self, estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas):
        self.pantalla.mostrarEncuesta(estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas)
    
    def tomarOpcionSalida(self, estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas):
        return self.generarCSV(estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas)

    def generarCSV(self,estadoActual, nombreCliente, duracion, descripcionEncuesta, descripcionPreguntas, descripcionRespuestas):
        with open('views/view.csv', 'w', encoding="UTF-8") as fp:
            contenido = f"""Nombre del cliente, Estado, Duracion\n{nombreCliente}, {estadoActual}, {duracion}\n"""

            for indice, pregunta in enumerate(descripcionPreguntas):
                    respuesta = descripcionRespuestas[indice]
                    contenido += f"Pregunta: {indice + 1}: {pregunta}, Respuesta: {indice + 1}: {respuesta.getDescripcionRespuesta()}\n"

            fp.write(contenido)
            pass