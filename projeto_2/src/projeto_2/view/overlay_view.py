import pygame

from projeto_2.constants import FECHAR_VITORIA, PAUSA_TOGGLE
from projeto_2.view.base_view import BaseView
from projeto_2.view.colors import Colors
from projeto_2.view.widget_views import Button, Text


class PopupView(BaseView):
    def __init__(
        self, *, area: tuple[int, int], widgets: list, largura_box=300, altura_box=200
    ):
        self.area = area  # Tamanho total da tela para o dimming
        self.widgets = widgets
        self.largura_box = largura_box
        self.altura_box = altura_box
        self.cor_bg = Colors.POPUP_BG
        self.cor_borda = Colors.POPUP_BORDER

    def _obter_box_rect(self) -> pygame.Rect:
        box_rect = pygame.Rect(0, 0, self.largura_box, self.altura_box)
        box_rect.center = (self.area[0] // 2, self.area[1] // 2)
        return box_rect

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        # 1. Dimming background
        overlay = pygame.Surface(self.area, pygame.SRCALPHA)
        overlay.fill(Colors.POPUP_OVERLAY)
        tela.blit(overlay, (0, 0))

        # 2. Caixa Centralizada
        box_rect = self._obter_box_rect()
        pygame.draw.rect(tela, self.cor_bg, box_rect, border_radius=10)
        pygame.draw.rect(tela, self.cor_borda, box_rect, width=2, border_radius=10)

        # 3. Widgets (desenhados relativos ao box)
        box_offset = (box_rect.x, box_rect.y)
        for widget in self.widgets:
            widget.desenhar(tela, box_offset)

    def handle_event(
        self, event: pygame.event.Event, offset: tuple[float, float] = (0, 0)
    ):
        box_rect = self._obter_box_rect()
        box_offset = (box_rect.x, box_rect.y)
        for widget in self.widgets:
            widget.handle_event(event, box_offset)


class PausaPopupView(PopupView):
    def __init__(self, *, area: tuple[int, int]):
        # Define os widgets internos (posicionados relativos ao Box de 300x200)
        self.btn_retomar = Button(
            rect=pygame.Rect(75, 120, 150, 40),
            texto="RETOMAR",
            evento_tipo=PAUSA_TOGGLE,
        )
        self.label_titulo = Text(
            pos=(0, 0),
            texto="PAUSADO",
            cor=Colors.WHITE,
            tamanho=36,
            centralizar_em_rect=pygame.Rect(0, 40, 300, 50),
        )

        super().__init__(
            area=area,
            widgets=[self.label_titulo, self.btn_retomar],
            largura_box=300,
            altura_box=200,
        )


class VitoriaPopupView(PopupView):
    def __init__(self, *, area: tuple[int, int], game_state_ro):
        self.game_state_ro = game_state_ro

        self.label_titulo = Text(
            pos=(0, 0),
            texto="VOCÊ VENCEU!",
            cor=Colors.BUTTON_SELECTED,
            tamanho=36,
            centralizar_em_rect=pygame.Rect(0, 30, 300, 50),
        )
        self.label_tempo = Text(
            pos=(0, 0),
            texto="",
            cor=Colors.WHITE,
            tamanho=24,
            centralizar_em_rect=pygame.Rect(0, 80, 300, 50),
        )
        self.btn_voltar = Button(
            rect=pygame.Rect(75, 140, 150, 40),
            texto="VOLTAR",
            evento_tipo=FECHAR_VITORIA,
        )

        super().__init__(
            area=area,
            widgets=[self.label_titulo, self.label_tempo, self.btn_voltar],
            largura_box=300,
            altura_box=220,
        )

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        # Atualiza o texto do tempo antes de desenhar
        tempo = self.game_state_ro.tempo_segundos
        minutos = tempo // 60
        segundos = tempo % 60
        self.label_tempo.texto = f"Seu Tempo: {minutos:02d}:{segundos:02d}"
        super().desenhar(tela, offset)
