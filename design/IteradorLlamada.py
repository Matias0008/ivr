from design.Iterator import Iterator
from models.Llamada import Llamada
from typing import Callable, TypeVar
T = TypeVar('T')

class IteradorLlamada(Iterator):
    llamadas: list[Llamada] = []
    posicion = 0
    filtros: list[Callable[[Llamada], bool]] = []

    def __init__(self, llamadas: list[Llamada], filtros: list[Callable[[Llamada], bool]]) -> None:
        self.filtros = filtros
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

    def cumpleFiltro(self) -> bool:
        for filtro in self.filtros:
            if not filtro(self.elementoActual()):
                return False
        return True
