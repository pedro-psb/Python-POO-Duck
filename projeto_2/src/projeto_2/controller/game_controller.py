import sys

import pygame

from projeto_2.constants import (
    CELULA_CLICK,
    DIFICULDADE_ALTERADA,
    PAUSA_TOGGLE,
    PLACAR_CLICK,
    REINICIAR_CLICK,
    VOLUME_ALTERADO,
)
from projeto_2.view.ranking_view import GameRankingView

from .audio_controller import AudioController
from .mapa_controller import MapaController


class GameController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        # O GameController processa eventos e use os sub-controllers para
        # atuar nos models. Os sub-controllers nao processam eventos, apenas
        # encapsulam certas atividades afins
        self.audio_controller = AudioController(model.game_state)
        self.mapa_controller = MapaController(
            model.game_state, mapa_quadrado=model.mapa
        )
        self.ranking_view = GameRankingView(
            self.view.tela, self.view.largura, self.view.altura
        )
        self.exibindo_ranking = False

    def iniciar_jogo(self):
        """Reinicia o jogo."""
        self.model.iniciar_jogo()

    def processar_evento_bruto(self, evento):
        """Repassa eventos do pygame para a view."""
        self.view.handle_event(evento)

    def processar_evento_jogo(self, evento):
        """Delega eventos de jogo para os sub-controllers atuarem nos models."""
        if evento.type == CELULA_CLICK:
            gx, gy = evento.pos
            if evento.button == 1:  # Esquerdo
                self.mapa_controller.handle_clique_esquerdo(gx, gy)
            elif evento.button == 3:  # Direito
                self.mapa_controller.handle_clique_direito(gx, gy)

        elif evento.type == REINICIAR_CLICK:
            print("Reiniciando jogo...")
            self.iniciar_jogo()

        elif evento.type == PLACAR_CLICK:
            print("Abrindo Placar...")
            self.exibindo_ranking = True

        elif evento.type == DIFICULDADE_ALTERADA:
            nome = evento.nome
            bombas = evento.bombas
            print(f"Mudando dificuldade para: {nome} ({bombas} bombas)")
            self.model.game_state.qtd_bombas = bombas
            self.model.game_state.dificuldade = nome
            self.iniciar_jogo()

        elif evento.type == VOLUME_ALTERADO:
            self.model.game_state.volume = evento.volume
            self.audio_controller.ajustar_volume(evento.volume)

        elif evento.type == PAUSA_TOGGLE:
            self.model.game_state.is_paused = not self.model.game_state.is_paused

        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE and self.exibindo_ranking:
                print("Voltando para o jogo...")
                self.exibindo_ranking = False

    def run(self):
        """Orquestra o loop principal do jogo."""
        self.audio_controller.iniciar_musica_fundo()

        rodando = True
        while rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

                self.processar_evento_bruto(evento)
                self.processar_evento_jogo(evento)

            if self.exibindo_ranking:
                # Pega a dificuldade que está salva no model do jogo
                # para filtrar os recordes
                dificuldade_atual = self.model.game_state.dificuldade
                self.ranking_view.desenhar(dificuldade_atual)
                pygame.display.flip()  # Força o pygame a atualizar a tela do ranking
            else:
                self.view.render()  # Desenha o campo minado normal

        pygame.quit()
        sys.exit()
