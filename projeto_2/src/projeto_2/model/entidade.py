from abc import ABC, abstractmethod

from projeto_2.validacao import inteiro_positivo


class Entidade(ABC):
    def __init__(self, id: int, status: bool, sprite: int):
        self._id = inteiro_positivo(id, nao_nulo=False)
        self._status = status
        self._sprite = inteiro_positivo(sprite, nao_nulo=False)

    @property
    def id(self):
        return self._id

    @property
    def status(self):
        return self._status

    @property
    def sprite(self):
        return self._sprite

    @abstractmethod
    def identificar(self) -> str:
        """Retorna uma string identificando o tipo de entidade."""
        pass
