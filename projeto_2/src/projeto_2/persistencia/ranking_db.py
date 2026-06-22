import json
import os

from .base import RepositorioRanking


class RepositorioRankingJSON(RepositorioRanking):
    """Implementação concreta que gerencia o Ranking usando um arquivo JSON."""

    def __init__(self, caminho_arquivo: str) -> None:
        self.caminho_arquivo = caminho_arquivo
        self._inicializar_arquivo()

    def _inicializar_arquivo(self) -> None:
        """Cria o arquivo JSON com uma lista vazia caso ele não exista."""
        if not os.path.exists(self.caminho_arquivo):
            with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def listar_melhores(self, dificuldade: str) -> list[dict]:
        """Lê o JSON, filtra pela dificuldade e ordena do menor tempo para o maior."""
        with open(self.caminho_arquivo, encoding="utf-8") as f:
            dados = json.load(f)

        # Filtrar e Ordenar
        filtrados = [p for p in dados if p["dificuldade"] == dificuldade]
        ranking_ordenado = sorted(filtrados, key=lambda x: x["tempo_segundos"])

        # Retorna apenas os 10 melhores tempos
        return ranking_ordenado[:10]

    def salvar_pontuacao(self, tempo: int, dificuldade: str) -> None:
        """Adiciona um novo recorde e salva no arquivo JSON."""
        with open(self.caminho_arquivo, encoding="utf-8") as f:
            dados = json.load(f)

        novo_registro = {
            "tempo_segundos": tempo,
            "dificuldade": dificuldade,
        }
        dados.append(novo_registro)

        with open(self.caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
