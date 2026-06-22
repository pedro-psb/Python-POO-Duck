import random

from projeto_2.validacao import inteiro_positivo

from .bomba import Bomba
from .celula import Celula
from .mapa import Mapa


class MapaQuadrado(Mapa):
    def __init__(self, colunas: int, linhas: int, total_bombas: int):
        self.colunas = colunas
        self.linhas = linhas
        self._mapa: list[list[Celula]] = []
        self._gerar_mapa()
        self.total_bombas = total_bombas

    def reset(self):
        """Reseta o mapa para um novo estado inicial."""
        self._gerar_mapa()

    def _gerar_mapa(self) -> None:
        """Gera a matriz de células ou reseta as existentes (status=True)."""
        # Verifica se a matriz precisa ser recriada devido a mudança de dimensões
        precisa_recriar = (
            not self._mapa
            or len(self._mapa) != self._linhas
            or (len(self._mapa) > 0 and len(self._mapa[0]) != self._colunas)
        )

        if precisa_recriar:
            self._mapa = []
            for y in range(self._linhas):
                linha = []
                for x in range(self._colunas):
                    address = y * self._colunas + x
                    linha.append(Celula(address=address, status=True))
                self._mapa.append(linha)
        else:
            for y in range(self._linhas):
                for x in range(self._colunas):
                    self._mapa[y][x].reset()

    @property
    def mapa(self) -> list[list[Celula]]:
        return self._mapa

    @property
    def colunas(self) -> int:
        return self._colunas

    @colunas.setter
    def colunas(self, valor: int):
        self._colunas = inteiro_positivo(valor, nao_nulo=True)

    @property
    def linhas(self) -> int:
        return self._linhas

    @linhas.setter
    def linhas(self, valor: int):
        self._linhas = inteiro_positivo(valor, nao_nulo=True)

    @property
    def total_bombas(self) -> int:
        return self._total_bombas

    @total_bombas.setter
    def total_bombas(self, quantidade: int) -> None:
        self._total_bombas = inteiro_positivo(quantidade, nao_nulo=True)

    def obter_celula(self, x: int, y: int) -> Celula | None:
        if 0 <= x < self._colunas and 0 <= y < self._linhas:
            return self._mapa[y][x]
        return None

    def distribuir_bombas(self, x_inicial: int, y_inicial: int):
        """
        Distribui bombas aleatoriamente no mapa, garantindo que a posição inicial
        (e seus vizinhos imediatos para uma experiência melhor) não contenha bomba.
        """
        posicoes_possiveis = []
        for y in range(self._linhas):
            for x in range(self._colunas):
                # Evita a célula clicada
                if abs(x - x_inicial) <= 1 and abs(y - y_inicial) <= 1:
                    continue
                posicoes_possiveis.append((x, y))

        quantidade = self.total_bombas
        if quantidade > len(posicoes_possiveis):
            quantidade = len(posicoes_possiveis)

        bombas_pos = random.sample(posicoes_possiveis, quantidade)

        for i, (bx, by) in enumerate(bombas_pos):
            celula = self.obter_celula(bx, by)
            if celula:
                celula.adicionar_entidade(Bomba(id=i, status=False, sprite=0))

        # Após distribuir, atualiza os valores de vizinhança
        self.contar_bombas_vizinhas()
        self.total_bombas = quantidade

    def contar_bombas_vizinhas(self):
        """
        Calcula a quantidade de bombas vizinhas para cada célula do mapa.
        Se a própria célula for uma bomba, seu valor de exibição será 0.
        """
        for y in range(self._linhas):
            for x in range(self._colunas):
                celula = self.obter_celula(x, y)
                if celula:
                    # Se a célula for uma bomba, não calculamos vizinhança para ela
                    if celula.obter_entidade(Bomba):
                        celula.valor = 0
                        continue

                    bombas = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue

                            vizinha = self.obter_celula(x + dx, y + dy)
                            if vizinha and vizinha.obter_entidade(Bomba):
                                bombas += 1

                    celula.valor = bombas

    def revelar(self, x: int, y: int) -> bool:
        """
        Revela a célula na posição [x, y].
        Se o valor da célula for 0, revela recursivamente as vizinhas.
        Retorna True se a célula revelada contiver uma bomba.
        """
        celula = self.obter_celula(x, y)

        if not celula or not celula.status:
            return False

        celula.cavar()  # Define status como False

        # Se encontrou uma bomba, retorna True
        if celula.obter_entidade(Bomba):
            return True

        # Se for uma célula vazia (valor 0), revela vizinhos recursivamente
        if celula.valor == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    self.revelar(x + dx, y + dy)

        return False

    def verificar_vitoria(self) -> bool:
        """Retorna True se todas as células seguras foram reveladas."""
        celulas_escondidas = sum(
            1 for linha in self._mapa for celula in linha if celula.status
        )
        return celulas_escondidas == self.total_bombas

    def __str__(self) -> str:
        res = ""
        for y in range(self._linhas):
            for x in range(self._colunas):
                celula = self._mapa[y][x]
                if celula.obter_entidade(Bomba):
                    res += "B "
                else:
                    res += f"{celula.valor} "
            res += "\n"
        return res
