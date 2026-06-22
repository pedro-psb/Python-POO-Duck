from abc import ABC, abstractmethod


class RepositorioRanking(ABC):
    """Classe Abstrata (Interface) que define o contrato do Ranking do jogo."""

    @abstractmethod
    def listar_melhores(self, dificuldade: str) -> list[dict]:
        """Deve ler a base de dados, filtrar por dificuldade e ordenar por tempo."""
        pass

    @abstractmethod
    def salvar_pontuacao(self, tempo: int, dificuldade: str) -> None:
        """Deve registrar um novo tempo recorde na base de dados."""
        pass
