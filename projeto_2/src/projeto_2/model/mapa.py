from abc import ABC, abstractmethod

from .celula import Celula


class Mapa(ABC):
    @property
    @abstractmethod
    def colunas(self) -> int:
        """Retorna a quantidade de colunas do mapa."""
        pass

    @property
    @abstractmethod
    def linhas(self) -> int:
        """Retorna a quantidade de linhas do mapa."""
        pass

    @property
    @abstractmethod
    def mapa(self) -> list[list[Celula]]:
        """Retorna a matriz de células do mapa."""
        pass

    @property
    @abstractmethod
    def total_bombas(self) -> int:
        """Retorna o número total de bombas do mapa."""
        pass

    @total_bombas.setter
    @abstractmethod
    def total_bombas(self, quantidade: int) -> None:
        """Define o número total de bombas do mapa."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reseta o mapa para um novo estado inicial."""
        pass

    @abstractmethod
    def obter_celula(self, x: int, y: int) -> Celula | None:
        """Retorna a célula na posição dada por x e y."""
        pass

    @abstractmethod
    def distribuir_bombas(
        self, x_inicial: int, y_inicial: int, quantidade: int
    ) -> None:
        """Distribui bombas de forma aleatória a partir de uma coordenada inicial."""
        pass

    @abstractmethod
    def verificar_vitoria(self) -> bool:
        """Retorna True se todas as células seguras foram reveladas."""
        pass

    @abstractmethod
    def revelar(self, x: int, y: int) -> bool:
        """Revela uma célula e retorna se ela possuía bomba (Game Over)."""
        pass
