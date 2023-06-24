from datetime import date, timedelta

import tkinter as tk
import libraries.ttkbootstrap as ttk 

from libraries.ttkbootstrap.tableview import Tableview
from libraries.ttkbootstrap.dialogs.dialogs import Messagebox

from models.Llamada import Llamada
font = ("JetBrains Mono", 14, "bold")

class PantallaConsultarEncuesta:
    def __init__(self, gestor):
        self.gestor = gestor

        self.root = ttk.Window(themename="flatly")
        self.root.title("Encuesta boundary")
        self.root.geometry("1280x720")
        self.root.resizable(0, 0)

        self.style = ttk.Style()
        self.style.configure(".", font=font)

        self.frame = tk.Frame(self.root)
        self.filtrosFrame: ttk.Frame
        self.llamadasFrame: ttk.Frame
        self.datosFrame: ttk.Frame
        self.opcionSalidaFrame: ttk.Frame
        self.btnConsultarEncuesta: ttk.Button
        self.btnBuscar: ttk.Button
        self.btnCancelar: ttk.Button
        self.btnVolver: ttk.Button
        self.fechaInicioLbl: ttk.Label
        self.fechaFinLbl: ttk.Label
        self.fechaInicioDate: ttk.DateEntry
        self.fechaFinDate: ttk.DateEntry
        self.fechaInicioTxt = date.today().strftime("%x")
        self.fechaFinTxt = (date.today() + timedelta(days=120)).strftime("%x")
        self.llamadasTableView: Tableview
        self.treeviewPreguntas: ttk.Treeview
        self.llamadaSeleccionada = []

    def eliminarVentanas(self):
        for frame in self.frame.winfo_children():
            frame.destroy()

    def opcionConsultarEncuesta(self):
        self.habilitarVentana()

    def habilitarVentana(self):
        self.eliminarVentanas()
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.btnConsultarEncuesta = ttk.Button(self.frame, text="Consultar encuesta", padding=15, command=self.gestor.consultarEncuesta)
        self.btnConsultarEncuesta.pack(anchor="center", pady=100, padx=100)
        self.root.mainloop()
    
    def tomarFechaInicio(self):
        self.fechaInicioTxt = self.fechaInicioDate.entry.get()

    def tomarFechaFin(self):
        self.fechaFinTxt = self.fechaFinDate.entry.get()
        self.tomarPeriodo()

    def habilitarFiltrosPorPeriodo(self):
        self.eliminarVentanas()
        self.filtrosFrame = ttk.Frame(self.frame)
        self.filtrosFrame.grid(column=0, row=0, pady=50, padx=50)

        # Configuracion para la fecha desde
        self.fechaInicioLbl = ttk.Label(self.filtrosFrame, text="Fecha inicio")
        self.fechaInicioLbl.grid(column=0, row=2, pady=(20, 5))

        self.fechaInicioDate= ttk.DateEntry(self.filtrosFrame, onChange=self.tomarFechaInicio)
        self.fechaInicioDate.entry.delete(0, tk.END)
        self.fechaInicioDate.entry.insert(tk.END, self.fechaInicioTxt)
        self.fechaInicioDate.grid(column=0, row=3)
        self.fechaInicioDate.entry.configure(state="readonly")
        self.fechaInicioDate.entry.configure(font=("JetBrains Mono", 14), width=12)
        self.fechaInicioDate.button.configure(padding=6)

        # Configuracion para la fecha fin
        self.fechaFinLbl = ttk.Label(self.filtrosFrame, text="Fecha fin")
        self.fechaFinLbl.grid(column=1 ,row=2, pady=(20, 5), padx=(80, 0))

        self.fechaFinDate = ttk.DateEntry(self.filtrosFrame, onChange=self.tomarFechaFin)
        self.fechaFinDate.entry.delete(0, tk.END)
        self.fechaFinDate.entry.insert(tk.END, self.fechaFinTxt)
        self.fechaFinDate.grid(column=1, row=3, padx=(80, 0))
        self.fechaFinDate.entry.configure(state="readonly")
        self.fechaFinDate.entry.configure(font=("JetBrains Mono", 14), width=12)
        self.fechaFinDate.button.configure(padding=6)

        self.tituloLbl = ttk.Label(self.filtrosFrame, text="Filtrar llamadas por periodo", font=("JetBrains Mono", 20, "bold"))
        self.tituloLbl.grid(column=0, row=0, columnspan=2, pady=(0, 20))
        self.separador = ttk.Separator(self.filtrosFrame, orient="horizontal")
        self.separador.grid(column=0, row=1, sticky="NSEW", columnspan=2)

        # Boton para accionar la busqueda
        self.btnBuscar = ttk.Button(self.filtrosFrame, text="Buscar", bootstyle="info", command=self.tomarPeriodo)
        self.btnBuscar.grid(column=0, row=4, columnspan=2, pady=(40, 0), sticky="NSEW")

        self.btnCancelar = ttk.Button(self.filtrosFrame ,text="Cancelar", bootstyle="danger", command=self.habilitarVentana)
        self.btnCancelar.grid(column=0, row=5, pady=(10, 0), sticky="NSEW", columnspan=2)
    
    def mostrarMensajeError(self, parent, message: str, title: str = ''):
        Messagebox.show_error(message=message, title=title, parent=parent)

    def tomarPeriodo(self):
        self.gestor.tomarPeriodo(self.fechaInicioTxt, self.fechaFinTxt)

    def mostrarLlamadas(self, llamadas: list[Llamada]):
        self.eliminarVentanas()

        # Definicion de los headers de nuestra tabla
        columnas = [
            {"text": "ID", "stretch": False },
            {"text": "Duracion", "stretch": True},
            {"text": "DNI Cliente", "stretch": True}
        ]
        
        filas = [
            (llamada.id, llamada.duracion, llamada.clienteDni)
            for llamada in llamadas
        ]

        self.llamadasFrame = ttk.Frame(self.frame)
        self.llamadasFrame.grid(column=0, row=0)
        llamadasFrameTitulo = ttk.Label(self.llamadasFrame, text="Llamadas", font=("JetBrains Mono", 18, "bold"))
        llamadasFrameTitulo.grid(column=0, row=0)
        llamadasFrameSubtitulo = ttk.Label(self.llamadasFrame, text=f"Periodo: {self.fechaInicioTxt} : {self.fechaFinTxt}").grid(column=0, row=1)

        self.llamadasTableView = Tableview(
            master=self.llamadasFrame,
            coldata=columnas,
            rowdata=filas,
            paginated=True,
            bootstyle="primary",
            autofit=True
        )

        self.llamadasTableView.view.configure(selectmode="browse")
        self.llamadasTableView.view.bind("<<TreeviewSelect>>", lambda event: self.tomarLlamada(llamadas=llamadas))
        self.llamadasTableView.grid(column=0, row=2, padx=50, pady=50)

        # Configuraciones para el boton volver
        self.btnVolver = ttk.Button(self.llamadasFrame ,text="Volver", command=self.habilitarFiltrosPorPeriodo, bootstyle="warning")
        self.btnVolver.grid(column=0, row=4, padx=(50, 150), pady=(10, 50), sticky="W")

    def tomarLlamada(self, llamadas: list[Llamada]):
        # Conseguimos el numero de fila seleccionado
        selected_iid = self.llamadasTableView.view.focus()
        llamada_index = self.llamadasTableView.view.index(selected_iid)
        self.llamadaSeleccionada = llamadas[llamada_index]

        self.btnTomarLlamada = ttk.Button(self.llamadasFrame, text="Tomar llamada", command=lambda: self.gestor.tomarLlamada(self.llamadaSeleccionada), bootstyle="success")
        self.btnTomarLlamada.grid(column=0, row=3, sticky="NSEW", padx=50)

        self.btnCancelar = ttk.Button(self.llamadasFrame ,text="Cancelar", bootstyle="danger", command=self.habilitarVentana)
        self.btnCancelar.grid(column=0, row=4, padx=(150, 50), pady=(10, 50), sticky="EW")

    def mostrarEncuesta (
            self,estadoActual,
            nombreCliente, 
            duracion, 
            descripcionEncuesta, 
            descripcionPreguntas,
            descripcionRespuestas
        ):

        self.eliminarVentanas()
        self.mostrarOpcionesSalida()

        # Posicionamos el frame para los datos
        self.datosFrame = ttk.LabelFrame(self.frame, text="Datos de la llamada")
        self.datosFrame.grid(column=0, row=0, padx=50, pady=50)

        # Definimos la estructura de la tabla
        columnas = [
            {"text": "Nombre del cliente", "stretch": True },
            {"text": "Duracion", "stretch": True},
            {"text": "Estado", "stretch": True}
        ]
        filas = [(nombreCliente, f"{duracion} minutos", estadoActual)]

        self.datosLlamadaTableView= Tableview(
            master=self.datosFrame,
            coldata=columnas,
            rowdata=filas,
            bootstyle="primary",
            height=1,
        )
        self.datosLlamadaTableView.grid(column=0, row=2, pady=(20, 0), columnspan=2, sticky="NSEW")
        self.datosLlamadaTableView.hbar.destroy()
        self.datosLlamadaTableView.view.config(selectmode="none")

        # Definimos la estructura de la tabla
        colummns = ("Pregunta", "Respuesta")
        self.treeviewPreguntas = ttk.Treeview(self.datosFrame, columns=colummns, show="headings", bootstyle="primary", selectmode="none", height=5)
        self.treeviewPreguntas.grid(column=0, row=3, pady=(20, 0))
        self.treeviewPreguntas.column(0, width=650)
        self.treeviewPreguntas.column(1, width=250)
        self.treeviewPreguntas.heading("Pregunta", text="Pregunta")
        self.treeviewPreguntas.heading("Respuesta", text="Respuesta")

        # Ahora tenemos que llenar de datos
        treeviewData = []
        for indice, pregunta in enumerate(descripcionPreguntas):
            treeviewData.append(
                ( pregunta, descripcionRespuestas[indice].getDescripcionRespuesta() )
            )

        # Ahora debemos insertar esos datos en la tabla
        for data in treeviewData:
            self.treeviewPreguntas.insert("", tk.END, values=data)

    def mostrarOpcionesSalida(self):
        # Frame general para las opciones
        self.opcionSalidaFrame = ttk.Labelframe(self.frame, text="Opciones", padding=20)
        self.opcionSalidaFrame.grid(column=0, row=5, padx=50, pady=(10, 50), sticky="NWSE")

        # Frame exclusivo para los botones
        self.grupoBotones = ttk.Frame(self.opcionSalidaFrame)
        self.grupoBotones.pack()
        
        # Frame exclusivo para los botones de generar resultados: imprimir y generar csv
        self.grupoBotonesResultados = ttk.Label(self.grupoBotones)
        self.grupoBotonesResultados.pack()

        # Frame exclusivo para los botones de volver y cancelar
        self.grupoBotonesSalida = ttk.Label(self.grupoBotones)
        self.grupoBotonesSalida.pack()

        # Botones para los resultados
        self.btnGenerarCsv = ttk.Button(self.grupoBotonesResultados ,text="Generar CSV", command=lambda: self.gestor.generarCSV(), width=12)
        self.btnGenerarCsv.pack(side="left", padx=(0, 5), pady=(0,5))

        self.btnImprimir = ttk.Button(self.grupoBotonesResultados ,text="Imprimir", width=12)
        self.btnImprimir.pack(side="left", padx=(0, 5), pady=(0,5))

        # Botones para la salida
        self.btnVolver = ttk.Button(self.grupoBotonesSalida ,text="Volver", bootstyle="warning", command=lambda: self.gestor.tomarPeriodo(self.fechaInicioTxt, self.fechaFinTxt), width=12)
        self.btnVolver.pack(side="left", padx=(0, 5))

        self.btnCancelar = ttk.Button(self.grupoBotonesSalida ,text="Cancelar", bootstyle="danger", command=self.habilitarVentana, width=12)
        self.btnCancelar.pack(side="left", padx=(0, 5))

    def tomarOpcionSalida(self):
        self.gestor.tomarOpcionSalida()