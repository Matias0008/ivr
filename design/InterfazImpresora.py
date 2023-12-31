import webbrowser

class InterfazImpresora:
    instancia = None

    @staticmethod
    def getInstancia():
        if InterfazImpresora.instancia == None:
            InterfazImpresora.instancia = InterfazImpresora()
        return InterfazImpresora.instancia
    
    def imprimir(self, *args: list[str]):
        # Generamos las respuestas y preguntas de manera dinamica
        nombreCliente, duracionLlamada, estado, pregunta, respuesta = args
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