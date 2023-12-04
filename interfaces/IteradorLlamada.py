from interfaces.Iterator import Iterator
from typing import TypeVar

from models.Llamada import Llamada

T = TypeVar('T')

class IteradorLlamada(Iterator):
    llamadas: list[Llamada] = []
    filtros: list[T] = []
    posicion = 0

    def __init__(self, llamadas: list[Llamada]) -> None:
        self.llamadas = llamadas

    def primero(self) -> None:
        return self.llamadas[0]
    
    def siguiente(self) -> None:
        llamada = self.llamadas[self.posicion]
        self.posicion += 1
        return llamada

    def haTerminado(self) -> bool:
        return self.posicion >= (len(self.llamadas) - 1)

    def elementoActual(self) -> Llamada:
        return self.llamadas[self.posicion]

    # def cumpleFiltro(self):
    #     for filtro in self.filtros:
    #         if not filtro(self.elementoActual()):
    #             return False
    #         return True