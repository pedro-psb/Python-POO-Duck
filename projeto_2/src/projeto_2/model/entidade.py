from abc import ABC, abstractmethod

from projeto_2.validacao import inteiro_positivo


class Entidade(ABC):
    def __init__(self, id: int, status: bool, sprite: int):
        self.id = id
        self._status = status
        self.sprite = sprite

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, valor: int):
        self._id = inteiro_positivo(valor, nao_nulo=False)

    @property
    def status(self):
        return self._status

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, valor: int):
        self._sprite = inteiro_positivo(valor, nao_nulo=False)

    @abstractmethod
    def identificar(self) -> str:
        """Retorna uma string identificando o tipo de entidade."""
        pass
