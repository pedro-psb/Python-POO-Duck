from typing import TypeVar

from projeto_2.validacao import inteiro_positivo

from .bandeira import Bandeira
from .bomba import Bomba
from .entidade import Entidade

T = TypeVar("T", bound=Entidade)


class Celula:
    def __init__(
        self, address: int, status: bool = True, valor: int = 0, sprite: int = 0
    ):
        """
        status: True para escondida (padrão), False para cavada.
        """
        self.address = address
        self._status = status
        self.valor = valor
        self.sprite = sprite
        self._entidades: list[Entidade] = []

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, novo_address: int):
        self._address = inteiro_positivo(novo_address, nao_nulo=False)

    @property
    def status(self):
        return self._status

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, novo_valor: int):
        self._valor = inteiro_positivo(novo_valor, nao_nulo=False)

    @property
    def sprite(self):
        return self._sprite

    @sprite.setter
    def sprite(self, novo_sprite: int):
        self._sprite = inteiro_positivo(novo_sprite, nao_nulo=False)

    @property
    def entidades(self) -> list[Entidade]:
        return self._entidades

    def reset(self):
        """Restaura a célula ao seu estado inicial escondido."""
        self._status = True
        self._valor = 0
        self._sprite = 0
        self._entidades.clear()

    def cavar(self):
        """
        Muda o status para False (cavada) se a célula estiver escondida (True).
        """
        if self._status:
            self._status = False
            # Define o sprite base como 'aberto' (index 1)
            self._sprite = 32 * 1

    def _tem_entidade_do_tipo(self, tipo: type[Entidade]) -> bool:
        return any(isinstance(e, tipo) for e in self._entidades)

    def adicionar_bandeira(self, bandeira: Bandeira):
        if self._tem_entidade_do_tipo(Bandeira):
            raise ValueError("Esta célula já possui uma bandeira.")
        self._entidades.append(bandeira)

    def adicionar_bomba(self, bomba: Bomba):
        if self._tem_entidade_do_tipo(Bomba):
            raise ValueError("Esta célula já possui uma bomba.")
        self._entidades.append(bomba)

    def remover_entidade(self, tipo: type[Entidade]):
        self._entidades = [e for e in self._entidades if not isinstance(e, tipo)]

    def obter_entidade(self, tipo: type[T]) -> T | None:
        for e in self._entidades:
            if isinstance(e, tipo):
                return e
        return None
