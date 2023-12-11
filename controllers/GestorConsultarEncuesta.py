from controllers.Database import *
from datetime import datetime
from enums.TipoReporte import TipoReporte
from design.IteradorLlamada import IteradorLlamada
from design.Iterator import Agregado

from models.Encuesta import Encuesta
from models.Llamada import Llamada
from design.InterfazImpresora import InterfazImpresora

from views.PantallaConsultarEncuesta import *
import csv

class GestorConsultarEncuesta(Agregado):
    opcionSalida: TipoReporte
    iteradorLlamada: IteradorLlamada
    llamadas: list[Llamada]

    def __init__(self) -> None:
        self.fechaFin: str
        self.fechaInicio: str
        self.llamadasDentroDePeriodo: List[Llamada]
        self.llamadaSeleccionada: Llamada
        self.encuestas: List[Encuesta]
        self.encuestaDeCliente: Encuesta
        self.session = DatabaseController().session

    def crearIterador(self):
        self.llamadas = self.session.query(Llamada).all()
        filtro_esDePeriodo = lambda llamada: llamada.esDePeriodo(self.fechaInicio, self.fechaFin)
        filtro_tieneEncuestaRespondida = lambda llamada: llamada.tieneEncuestaRespondida()
        return IteradorLlamada(self.llamadas, [filtro_esDePeriodo, filtro_tieneEncuestaRespondida])

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

        self.buscarLlamadasDentroDePeriodo()

    def validarPeriodo(self):
        return self.fechaFin > self.fechaInicio

    def buscarLlamadasDentroDePeriodo(self): #8
        self.iteradorLlamada = self.crearIterador()
        self.llamadasDentroDePeriodo = []

        # Implementar Iterator
        elementoActual = self.iteradorLlamada.primero()
        while not self.iteradorLlamada.haTerminado():
            elementoActual = self.iteradorLlamada.elementoActual()

            if self.iteradorLlamada.cumpleFiltro():
                self.llamadasDentroDePeriodo.append(elementoActual)
            
            self.iteradorLlamada.siguiente()

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
        self.opcionSalida = tipoReporte
        self.generarReporte()

    def generarReporte(self) -> None:
        match self.opcionSalida:
            case TipoReporte.CSV:
                self.crearCSV(self.nombreCliente, self.duracion, self.estadoActual, self.descripcionPreguntas, self.descripcionRespuestas)
                self.pantalla.mostrarMensajeSatisfactorio("Se genero el archivo CSV correctamente")
            case TipoReporte.IMPRESO:
                interfazImpresora = InterfazImpresora.getInstancia()
                interfazImpresora.imprimir(self.nombreCliente, self.duracion, self.estadoActual, self.descripcionPreguntas, self.descripcionRespuestas)
                self.pantalla.mostrarMensajeSatisfactorio("Se genero el archivo a imprimir correctamente")

    def crearCSV(self, nombreCliente: str, duracionLlamada: int, estado: str, pregunta: list, respuesta: list):
        encabezados = ["Nombre del cliente", "Duración", "Estado"]

        # Añadir encabezados de preguntas y respuestas
        for i in range(len(pregunta)):
            encabezados.append('Pregunta')
            encabezados.append('Respuesta')

        datos = [nombreCliente, duracionLlamada, estado] + [val for pair in zip(pregunta, respuesta) for val in pair]

        # Abrir archivo CSV en modo escritura
        with open('reporte.csv', 'w', newline='', encoding="UTF-8") as archivo:
            writer = csv.writer(archivo)

            # Escribir encabezados en el archivo CSV
            writer.writerow(encabezados)

            # Escribir datos en el archivo CSV
            writer.writerow(datos)

    def finDeCU(self):
        return exit()
    
