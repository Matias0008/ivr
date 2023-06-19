import tkinter as tk
import style.ttkbootstrap as ttk
from style.ttkbootstrap.tableview import Tableview

class EncuestaBoundary:
    frame: ttk.Frame
    btnConsultarEncuesta: ttk.Button
    btnBuscar: ttk.Button
    filtrosFrame: ttk.Frame
    fechaInicioLbl: ttk.Label
    fechaInicioDate: ttk.DateEntry
    fechaFinLbl: ttk.Label
    fechaFinDate: ttk.Label

    def __init__(self, controller):
        self.controller = controller

        font = ("JetBrains Mono", 14, "bold")
        self.root = ttk.Window(themename="flatly")
        self.root.title("Encuesta boundary")
        self.root.resizable(0, 0)

        self.style = ttk.Style()
        self.style.configure(".", font=font)

        # Frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack()

    def opcionConsultarEncuesta(self):
        self.habilitarVentana()

    def habilitarVentana(self):
        self.btnConsultarEncuesta = ttk.Button(self.frame, text="Consultar encuesta", style="ConsultarEncuesta.TButton", padding=15, command=self.controller.consultarEncuesta)
        self.btnConsultarEncuesta.pack(anchor="center", pady=100, padx=100)
        self.root.mainloop()

    def habilitarFiltrosPorPeriodo(self):
        self.btnConsultarEncuesta.destroy()
        self.filtrosFrame = ttk.Frame(self.frame)
        self.filtrosFrame.grid(column=0, row=0, pady=50, padx=50)

        self.tituloLbl = ttk.Label(self.filtrosFrame, text="Filtrar llamadas por periodo", font=("JetBrains Mono", 20, "bold"))
        self.tituloLbl.grid(column=0, row=0, columnspan=2, pady=(0, 20))
        self.separador = ttk.Separator(self.filtrosFrame, orient="horizontal")
        self.separador.grid(column=0, row=1, sticky="NSEW", columnspan=2)

        # Configuracion para la fecha desde
        self.fechaInicioLbl = ttk.Label(self.filtrosFrame, text="Fecha inicio")
        self.fechaInicioLbl.grid(column=0, row=2, pady=(20, 5))

        self.fechaInicioDate= ttk.DateEntry(self.filtrosFrame)
        self.fechaInicioDate.grid(column=0, row=3)
        self.fechaInicioDate.entry.configure(font=("JetBrains Mono", 14), width=12)
        self.fechaInicioDate.button.configure(padding=6)

        # Configuracion para la fecha fin
        self.fechaFinLbl = ttk.Label(self.filtrosFrame, text="Fecha fin")
        self.fechaFinLbl.grid(column=1 ,row=2, pady=(20, 5), padx=(80, 0))

        self.fechaFinDate = ttk.DateEntry(self.filtrosFrame)
        self.fechaFinDate.grid(column=1, row=3, padx=(80, 0))
        self.fechaFinDate.entry.configure(font=("JetBrains Mono", 14), width=12)
        self.fechaFinDate.button.configure(padding=6)

        # Boton para accionar la busqueda
        self.btnBuscar = ttk.Button(self.filtrosFrame, text="Buscar", bootstyle="info", command=self.buscarLlamadas)
        self.btnBuscar.grid(column=0, row=4, columnspan=2, pady=(40, 0), sticky="NSEW")

    def tomarFechaInicio(self, event):
        print("Tocaste la fecha de inicio")

    def buscarLlamadas(self):
        coldata = [
        {"text": "ID", "stretch": False },
        {"text": "Nombre", "stretch": True},
        {"text": "Apellido", "stretch": True},
        ]

        rowdata = [] 
        self.clientesFrame = ttk.Frame(self.frame)
        self.clientesFrame.grid(column=0, row=0)
        self.tableView = Tableview(
            master=self.clientesFrame,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle="primary",
            autofit=True
        )

        self.tableView.grid(column=0, row=0, padx=50, pady=50)
        self.filtrosFrame.destroy()

    def mostrarEncuestas(self):
        self.controller.mostrarEncuestas()