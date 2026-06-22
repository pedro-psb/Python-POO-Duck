import os

import pygame

from .base_view import BaseView
from .colors import Colors
from .mapa_view import MapaView
from .menu_view import MenuView
from .ranking_view import GameRankingView
from .widget_views import PausaPopupView


class GameView(BaseView):
    def __init__(self, game_model_ro, largura: int = 800, altura: int = 600):
        pygame.init()
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Campo Minado - Pygame")

        self.spritesheet = self._carregar_spritesheet()
        self.cor_fundo = Colors.BACKGROUND
        self.game_model_ro = game_model_ro

        # Configurações de layout
        self.largura_info = largura // 4
        self.largura_area_mapa = largura - self.largura_info

        # Sub-views
        self.mapa_view = MapaView(
            mapa_ro=game_model_ro.mapa,
            spritesheet=self.spritesheet,
            area=(self.largura_area_mapa, self.altura),
            tamanho_celula=32,
        )
        self.menu_view = MenuView(
            game_state_ro=game_model_ro.game_state,
            area=(self.largura_info, self.altura),
        )

        # Overlays
        self.pausa_popup = PausaPopupView(area=(largura, altura))
        self.ranking_popup = GameRankingView(area=(largura, altura))

    @property
    def offset(self) -> tuple[float, float]:
        return 0.0, 0.0

    @property
    def offset_menu(self) -> tuple[float, float]:
        return float(self.largura_area_mapa), 0.0

    @property
    def offset_mapa(self) -> tuple[float, float]:
        return 0.0, 0.0

    @property
    def tamanho_celula(self):
        return self.mapa_view.tamanho_celula

    def converter_tela_para_grade(self, pos):
        """Converte coordenadas da tela para (x, y) da grade."""
        return self.mapa_view.converter_tela_para_grade(pos, self.offset_mapa)

    def handle_event(self, event, offset=(0, 0)):
        """
        Trata eventos. Se um overlay estiver ativo, bloqueia eventos para o jogo.
        """
        gs = self.game_model_ro.game_state

        if gs.is_paused:
            self.pausa_popup.handle_event(event)
            return  # Bloqueia propagação

        if gs.exibindo_ranking:
            self.ranking_popup.handle_event(event)
            return  # Bloqueia propagação

        # Fluxo normal
        self.mapa_view.handle_event(event, self.offset_mapa)
        self.menu_view.handle_event(event, self.offset_menu)

    def desenhar(self, tela: pygame.Surface, offset=(0, 0)):
        """Renderiza todos os componentes na tela, incluindo overlays."""
        # 1. Camada de Jogo
        self.mapa_view.desenhar(tela, self.offset_mapa)
        self.menu_view.desenhar(tela, self.offset_menu)

        # 2. Camada de Overlays
        if self.game_model_ro.game_state.is_paused:
            self.pausa_popup.desenhar(tela)
        elif self.game_model_ro.game_state.exibindo_ranking:
            self.ranking_popup.desenhar(tela)

    def render(self):
        """
        Executa o ciclo completo de renderização: limpar, desenhar e atualizar.
        """
        self.limpar_tela()
        self.desenhar(self.tela)
        self.atualizar()

    def _carregar_spritesheet(self):
        caminho_sprites = os.path.join("imagens", "New Piskel.png")
        try:
            return pygame.image.load(caminho_sprites).convert_alpha()
        except Exception:
            return pygame.Surface((32 * 20, 32))

    def limpar_tela(self):
        self.tela.fill(self.cor_fundo)

    def atualizar(self):
        pygame.display.flip()
