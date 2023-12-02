import csv

from datetime import datetime

from views.PantallaConsultarEncuesta import *
from controllers.Database import *

from models.Llamada import Llamada
from models.Encuesta import Encuesta
from interfaces.Strategy import  EstrategiaCSV, Estrategia, EstrategiaImprimir
from interfaces.Strategy import TipoReporte

class GestorConsultarEncuesta:
    estrategia: Estrategia

    def __init__(self) -> None:
        self.fechaFin: str
        self.fechaInicio: str
        self.llamadasDentroDePeriodo: List[Llamada]
        self.llamadaSeleccionada: Llamada
        self.encuestas: List[Encuesta]
        self.encuestaDeCliente: Encuesta
        self.session = DatabaseController().session

    def setPantalla(self, pantalla: PantallaConsultarEncuesta):
        self.pantalla = pantalla

    def consultarEncuesta(self): #3
        self.pantalla.habilitarFiltrosPorPeriodo()
    
    def tomarPeriodo(self, fechaInicio: str, fechaFin: str): #7
        # Transformamos de string a un tipo de dato de fecha
        self.fechaInicio = datetime.strptime(fechaInicio, "%x")
        self.fechaFin = datetime.strptime(fechaFin, "%x")

        # Validacion para que no se pueda insertar una fecha fin menor que la de inicio
        if not self.validarPeriodo():
            return self.pantalla.mostrarMensajeError(parent=self.pantalla.filtrosFrame,message="La fecha de fin es menor que la fecha de inicio", title="Fecha  de fin incorrecta")

        self.buscarLlamadasDentroDePeriodo(self.fechaInicio, self.fechaFin)

    def validarPeriodo(self):
        return self.fechaFin > self.fechaInicio

    def buscarLlamadasDentroDePeriodo(self, fechaInicio: str, fechaFin: str): #8
        # Obteniendo las llamadas con la base de datos
        llamadas: List[Llamada] = self.session.query(Llamada).all()

        # Conseguimos las llamadas que esten dentro de un periodo
        self.llamadasDentroDePeriodo = []
        for llamada in llamadas:
            if llamada.esDePeriodo(fechaInicio, fechaFin) and llamada.tieneEncuestaRespondida():
                self.llamadasDentroDePeriodo.append(llamada)

        # Si no encontramos ninguna llamada lanzamos un mensaje de error
        if (len(self.llamadasDentroDePeriodo) == 0):
            return self.pantalla.mostrarMensajeError(parent=self.pantalla.filtrosFrame,message="No hay llamadas dentro del periodo", title="No hay llamadas")

        self.mostrarLlamadas()

    def mostrarLlamadas(self): #13
        return self.pantalla.mostrarLlamadas(self.llamadasDentroDePeriodo)

    def tomarLlamada(self, llamadaSeleccionada: Llamada): #16
        self.llamadaSeleccionada = llamadaSeleccionada
        self.obtenerDatosLlamada()

    def obtenerDatosLlamada(self): #17
        # Primero obtenemos los datos de la llamada
        self.estadoActual, self.nombreCliente = self.llamadaSeleccionada.getNombreClienteDeLlamadaYEstadoActual()
        self.duracion = self.llamadaSeleccionada.getDuracion()

        # Luego obtenemos los datos de la encuesta
        self.descripcionEncuesta, self.descripcionPreguntas, self.descripcionRespuestas = self.obtenerDatosEncuesta()
        self.mostrarEncuesta()
    
    def obtenerDatosEncuesta(self): #25
        self.descripcionRespuestas = self.llamadaSeleccionada.getRespuestas()

        # Me conecto a la base de datos para obtener todas las encuestas
        encuestaCliente = []
        self.encuestas = self.session.query(Encuesta).all()

        for encuesta in self.encuestas:
            if encuesta.esEncuestaDeCliente(self.llamadaSeleccionada):
                encuestaCliente = encuesta

        self.descripcionEncuesta = encuestaCliente.getDescripcionEncuesta()
        self.descripcionPreguntas = encuestaCliente.armarEncuesta()
        return [self.descripcionEncuesta, self.descripcionPreguntas, self.descripcionRespuestas]
    
    def mostrarEncuesta(self): #35
        self.pantalla.mostrarEncuesta (
            self.estadoActual,
            self.nombreCliente,
            self.duracion,
            self.descripcionEncuesta,
            self.descripcionPreguntas,
            self.descripcionRespuestas
        )

    def tomarOpcionSalida(self, tipoReporte: TipoReporte): #39
        self.estrategia = self.crearEstrategia(tipoReporte) 
        return self.generarReporte()
    
    def generarReporte(self) -> None:
        self.estrategia.generarReporte(self.nombreCliente, self.duracion, self.estadoActual, self.descripcionPreguntas, self.descripcionRespuestas)
        self.pantalla.mostrarMensajeSatisfactorio(self.estrategia.mostrarMensajeSalida())
        # return self.finDeCU()

    def crearEstrategia(self, tipoReporte: TipoReporte) -> Estrategia:
        match tipoReporte:
            case TipoReporte.CSV:
                return EstrategiaCSV()
            case TipoReporte.IMPRESO:
                return EstrategiaImprimir()

    def finDeCU(self):
        return exit()