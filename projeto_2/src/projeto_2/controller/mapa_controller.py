from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.persistencia.ranking_db import RepositorioRankingJSON


class MapaController:
    def __init__(self, game_state, mapa_quadrado):
        self._mapa = mapa_quadrado
        self._game_state = game_state

    @property
    def mapa(self):
        return self._mapa

    @mapa.setter
    def mapa(self, novo_mapa):
        self._mapa = novo_mapa

    def handle_clique_esquerdo(self, x: int, y: int):
        """Revelar célula."""
        if self._game_state.jogo_finalizado:
            return

        celula = self._mapa.obter_celula(x, y)
        if not celula:
            return

        # Não permite revelar se a célula tiver uma bandeira
        if celula.obter_entidade(Bandeira):
            return

        if self._game_state.primeiro_clique:
            self._mapa.distribuir_bombas(x, y)
            self._game_state.primeiro_clique = False
            print("Bombas distribuídas.")
            # Inicia o relógio no primeiro clique
            self._game_state.iniciar_timer()

        if self._mapa.revelar(x, y):
            # Game Over
            self._game_state.jogo_finalizado = True
            self._game_state.parar_timer()

            # Executa explodir apenas na bomba que foi clicada
            bomba_clicada = celula.obter_entidade(Bomba)
            if bomba_clicada:
                bomba_clicada.explodir()

            # Revela todas as células do mapa
            print("GAME OVER! Revelando tabuleiro...")
            for ry in range(self._mapa.linhas):
                for rx in range(self._mapa.colunas):
                    c = self._mapa.obter_celula(rx, ry)
                    if c:
                        c.cavar()
        elif self._mapa.verificar_vitoria():
            print("VITÓRIA!")
            self._game_state.jogo_finalizado = True
            self._game_state.parar_timer()

            # Salva o tempo no ranking
            repo = RepositorioRankingJSON("ranking.local.json")
            repo.salvar_pontuacao(
                tempo=self._game_state.tempo_segundos,
                dificuldade=self._game_state.dificuldade,
            )

    def handle_clique_direito(self, x: int, y: int):
        """Adicionar/Alternar bandeira."""
        if self._game_state.jogo_finalizado:
            return

        celula = self._mapa.obter_celula(x, y)
        if not celula:
            return

        if celula.status:
            if celula.obter_entidade(Bandeira):
                celula.remover_entidade(Bandeira)
            else:
                nova_bandeira = Bandeira(id=celula.address, status=True, sprite=0)
                celula.adicionar_bandeira(nova_bandeira)
