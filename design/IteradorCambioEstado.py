from design.Iterator import Iterator
from models.CambioEstado import CambioEstado 

class IteradorCambioEstado(Iterator):
    cambioEstado: list[CambioEstado] = []
    posicion = 0

    def __init__(self, cambioEstado: list[CambioEstado]) -> None:
        self.cambioEstado = cambioEstado

    def primero(self) -> CambioEstado:
        return self.cambioEstado[0]

    def siguiente(self) -> None:
        cambioEstado = self.cambioEstado[self.posicion]
        self.posicion += 1
        return cambioEstado

    def haTerminado(self) -> bool:
        return self.posicion >= (len(self.cambioEstado) - 1)
    
    def elementoActual(self) -> CambioEstado:
        return self.cambioEstado[self.posicion]