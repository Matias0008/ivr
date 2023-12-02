from abc import ABC, abstractmethod
import csv

class Estrategia(ABC):
    @abstractmethod
    def generarReporte(self, encabezado: list['str'], pregunta: list['str'], respuesta: list['str']):
        pass

class EstrategiaCSV(Estrategia):
    def generarReporte(self, nombreCliente: str, duracionLlamada: int, estado: str, pregunta: list['str'], respuesta: list['str']):
        encabezados = ["Nombre del cliente", "Duración", "Estado", "Pregunta", "Respuesta"]
        datos = [[nombreCliente, duracionLlamada, estado]]

        for indice, pregunta in enumerate(pregunta):
            respuesta = respuesta[indice]
            datos[0].append(pregunta)
            datos[0].append(respuesta)

            if indice != len(pregunta) - 1:
                encabezados.append("Pregunta")
                encabezados.append("Respuesta")

        with open("view.csv", mode='w', newline='', encoding="UTF-8") as archivo:
            writer = csv.writer(archivo)
            writer.writerow(encabezados)
            writer.writerows(datos)

class EstrategiaImprimir(Estrategia):
    def generarReporte(self, encabezado: list['str'], pregunta: list['str']):
        pass