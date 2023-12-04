from abc import ABC, abstractmethod
import webbrowser
import csv

class Estrategia(ABC):
    @abstractmethod
    def generarReporte(self, nombreCliente: str, duracionLlamada: int, estado: str, pregunta: list, respuesta: list):
        pass

    @abstractmethod
    def mostrarMensajeSalida(self):
        pass

class EstrategiaCSV(Estrategia):
    def generarReporte(self, nombreCliente: str, duracionLlamada: int, estado: str, pregunta: list, respuesta: list):
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

    def mostrarMensajeSalida(self):
        return "Se genero el archivo CSV de manera correcta"

class EstrategiaImprimir(Estrategia):
    def generarReporte(self, nombreCliente: str, duracionLlamada: int, estado: str, pregunta: list, respuesta: list):    

        # Generamos las respuestas y preguntas de manera dinamica
        preguntasYRespuestas = "" 
        for i in range(len(pregunta)):
            preguntasYRespuestas += f"""
            <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                  {pregunta[i]}
                </th>
                <td class="px-6 py-4">{respuesta[i]}</td>
            </tr>
            """

        # Crear un archivo HTML con los datos
        contenidoHTML = f"""
        <html>
          <head>
            <script src="https://cdn.tailwindcss.com"></script>
            <title>Impresion de datos</title>
          </head>
          <body class="min-h-screen w-full flex items-center justify-center">
            <div class="relative overflow-x-auto">
              <div class="inline-flex items-center justify-center w-full mb-6">
                <hr
                  class="w-full h-px my-8 bg-gray-200 border-0 dark:bg-gray-700 opacity-40"
                />
                <span
                  class="absolute px-6 py-1 font-medium text-white -translate-x-1/2 bg-white left-1/2 dark:bg-gray-700 rounded-lg text-[25px]"
                  >Datos de la encuesta</span
                >
              </div>
              <table class="w-full text-xl text-left rtl:text-right text-gray-500 dark:text-gray-400">
                <thead class="text-xl text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th scope="col" class="px-6 py-3">Nombre del cliente</th>
                    <th scope="col" class="px-6 py-3">Duracion de la llamada</th>
                    <th scope="col" class="px-6 py-3">Estado de la llamada</th>
                  </tr>
                </thead>
                <tbody>
                  <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white"
                    >{nombreCliente}</th>
                  <td class="px-6 py-4">{duracionLlamada} minutos</td>
                  <td class="px-6 py-4">{estado}</td>
                  </tr>
                </tbody>
              </table>
              <div class="inline-flex items-center justify-center w-full mt-6">
                <hr
                  class="w-full h-px my-8 bg-gray-200 border-0 dark:bg-gray-700 opacity-40"
                />
                <span
                  class="absolute px-6 py-1 font-medium text-white -translate-x-1/2 bg-white left-1/2 dark:bg-gray-700 rounded-lg text-[25px]"
                  >Preguntas y respuestas</span
                >
              </div>
              <!-- Otra tabla -->
              <table class="w-full text-xl text-left rtl:text-right text-gray-500 dark:text-gray-400 mt-6">
                <thead class="text-xl text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                  <tr>
                    <th scope="col" class="px-6 py-3">Pregunta</th>
                    <th scope="col" class="px-6 py-3">Respuesta</th>
                  </tr>
                </thead>
                <tbody>
                  {preguntasYRespuestas}
                </tbody>
              </table>
          </body>
        </html>
        """

        # Guardar el contenido en un archivo HTML
        with open("impresion_datos.html", "w") as file:
            file.write(contenidoHTML)

        # Abrir el archivo en el navegador para impresión
        webbrowser.open("impresion_datos.html")

    def mostrarMensajeSalida(self):
        return "Se imprimio el reporte de manera correcta"