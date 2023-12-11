from interfaces.Iterator import Iterator
from models.Llamada import Llamada
from typing import Callable, TypeVar

T = TypeVar('T')

class IteradorLlamada(Iterator):
    filtros: list[Callable[[Llamada], bool]] = []
    llamadas: list[Llamada] = []
    posicion = 0

    def __init__(self, llamadas: list[Llamada], filtros: list[Callable[[Llamada], bool]]) -> None:
        self.filtros = filtros
        self.llamadas = llamadas

    def primero(self) -> None:
        return self.llamadas[0]
    
    def siguiente(self) -> None:
        self.posicion += 1

    def haTerminado(self) -> bool:
        return self.posicion >= (len(self.llamadas) - 1)

    def elementoActual(self) -> Llamada:
        return self.llamadas[self.posicion]

    def cumpleFiltro(self) -> bool:
        for filtro in self.filtros:
            if not filtro(self.elementoActual()):
                return False
        return True
