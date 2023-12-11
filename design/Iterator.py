from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class Iterator(ABC, Generic[T]):
    @abstractmethod
    def primero(self) -> None:
        pass

    @abstractmethod
    def siguiente(self) -> None:
        pass

    @abstractmethod
    def elementoActual(self) -> T:
        pass

    @abstractmethod
    def haTerminado(self) -> bool:
        pass

class Agregado(ABC):
    @abstractmethod
    def crearIterador(self) -> Iterator:
        pass