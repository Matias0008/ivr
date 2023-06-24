import csv
import tkinter as tk

from datetime import datetime

from views.PantallaConsultarEncuesta import *
from controllers.Database import *

from models.Llamada import Llamada
from models.Encuesta import Encuesta

class GestorConsultarEncuesta:
    def __init__(self) -> None:
        self.pantalla: PantallaConsultarEncuesta
        self.fechaFin: str
        self.fechaInicio: str
        self.llamadasDentroDePeriodo: List[Llamada]
        self.llamadaSeleccionada: Llamada
        self.encuestas: List[Encuesta]
        self.encuestaDeCliente: Encuesta

    def setPantalla(self, pantalla: PantallaConsultarEncuesta):
        self.pantalla = pantalla

    def consultarEncuesta(self):
        self.pantalla.habilitarFiltrosPorPeriodo()
    
    def tomarPeriodo(self, fechaInicio: str, fechaFin: str):
        # Transformamos de string a un tipo de dato de fecha
        self.fechaInicio = datetime.strptime(fechaInicio, "%x")
        self.fechaFin = datetime.strptime(fechaFin, "%x")

        # Validacion para que no se pueda insertar una fecha fin menor que la de inicio
        if (self.fechaFin < self.fechaInicio):
            return self.pantalla.mostrarMensajeError(parent=self.pantalla.filtrosFrame,message="La fecha de fin es menor que la fecha de inicio", title="Fecha  de fin incorrecta")

        self.buscarLlamadasDentroDePeriodo(self.fechaInicio, self.fechaFin)

    def buscarLlamadasDentroDePeriodo(self, fechaInicio: str, fechaFin: str):
        # Obteniendo las llamadas con la base de datos
        db = DatabaseController()
        db.connect()
        llamadas: List[Llamada] = db.session.query(Llamada).all()

        # Conseguimos las llamadas que esten dentro de un periodo
        self.llamadasDentroDePeriodo = []
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
        self.estadoActual, self.nombreCliente = self.llamadaSeleccionada.getNombreClienteDeLlamadaYEstadoActual()
        self.duracion = self.llamadaSeleccionada.getDuracion()

        # Luego obtenemos los datos de la encuesta
        self.descripcionEncuesta, self.descripcionPreguntas, self.descripcionRespuestas = self.obtenerDatosEncuesta()
        self.mostrarEncuesta()
    
    def obtenerDatosEncuesta(self):
        descripcionRespuestas = self.llamadaSeleccionada.getRespuestas()

        # Me conecto a la base de datos para obtener todas las encuestas
        db = DatabaseController()
        db.connect()
        encuestaCliente = []
        self.encuestas = db.session.query(Encuesta).all()

        for encuesta in self.encuestas:
            if encuesta.esEncuestaDeCliente(self.llamadaSeleccionada):
                encuestaCliente = encuesta

        descripcionEncuesta = encuestaCliente.getDescripcionEncuesta()
        descripcionPreguntas = encuestaCliente.armarEncuesta()
        return [descripcionEncuesta, descripcionPreguntas, descripcionRespuestas]
    
    def mostrarEncuesta(self):
        self.pantalla.mostrarEncuesta (
            self.estadoActual,
            self.nombreCliente,
            self.duracion,
            self.descripcionEncuesta,
            self.descripcionPreguntas,
            self.descripcionRespuestas
        )

    def tomarOpcionSalida(self):
        return self.generarCSV()

    def generarCSV(self):
        encabezados = ["Nombre del cliente", "Duración", "Estado", "Pregunta", "Respuesta"]
        datos = [[self.nombreCliente, self.duracion, self.estadoActual]]

        for indice, pregunta in enumerate(self.descripcionPreguntas):
            respuesta = self.descripcionRespuestas[indice]
            datos[0].append(pregunta)
            datos[0].append(respuesta.getDescripcionRespuesta())

            if indice != len(self.descripcionPreguntas) - 1:
                encabezados.append("Pregunta")
                encabezados.append("Respuesta")

        with open("view.csv", mode='w', newline='') as archivo:
            writer = csv.writer(archivo)
            writer.writerow(encabezados)
            writer.writerows(datos)