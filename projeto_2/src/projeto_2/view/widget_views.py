import pygame

from projeto_2.constants import PAUSA_TOGGLE, VOLUME_ALTERADO
from projeto_2.utils import post_evento

from .base_view import BaseView
from .colors import Colors


class Box(BaseView):
    def __init__(self, *, rect: pygame.Rect, cor: tuple[int, int, int]):
        self.rect = rect
        self.cor = cor

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        abs_rect = self.rect.move(offset)
        pygame.draw.rect(tela, self.cor, abs_rect)


class HorizontalSeparator(BaseView):
    def __init__(
        self,
        *,
        x_inicio: int,
        x_fim: int,
        y: int,
        cor: tuple[int, int, int],
        largura: int = 2,
    ):
        self.x_inicio = x_inicio
        self.x_fim = x_fim
        self.y = y
        self.cor = cor
        self.largura = largura

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        ox, oy = offset
        pygame.draw.line(
            tela,
            self.cor,
            (self.x_inicio + ox, self.y + oy),
            (self.x_fim + ox, self.y + oy),
            self.largura,
        )


class VerticalSeparator(BaseView):
    def __init__(
        self,
        *,
        x: int,
        y_inicio: int,
        y_fim: int,
        cor: tuple[int, int, int],
        largura: int = 2,
    ):
        self.x = x
        self.y_inicio = y_inicio
        self.y_fim = y_fim
        self.cor = cor
        self.largura = largura

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        ox, oy = offset
        pygame.draw.line(
            tela,
            self.cor,
            (self.x + ox, self.y_inicio + oy),
            (self.x + ox, self.y_fim + oy),
            self.largura,
        )


class Text(BaseView):
    def __init__(
        self,
        *,
        pos: tuple[int, int],
        texto: str,
        cor: tuple[int, int, int],
        tamanho: int = 20,
        bold: bool = True,
        fonte_nome: str = "Arial",
        centralizar_em_rect: pygame.Rect = None,
    ):
        self.pos = pos
        self.texto = texto
        self.cor = cor
        self.fonte = pygame.font.SysFont(fonte_nome, tamanho, bold=bold)
        self.centralizar_em_rect = centralizar_em_rect

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        ox, oy = offset
        txt_surf = self.fonte.render(self.texto, True, self.cor)
        if self.centralizar_em_rect:
            abs_rect = self.centralizar_em_rect.move(offset)
            txt_rect = txt_surf.get_rect(center=abs_rect.center)
            tela.blit(txt_surf, txt_rect)
        else:
            tela.blit(txt_surf, (self.pos[0] + ox, self.pos[1] + oy))


class Button(BaseView):
    def __init__(
        self, *, rect: pygame.Rect, texto: str, evento_tipo: int, **evento_data
    ):
        self.rect = rect
        self.cor_fundo = Colors.BUTTON_BG
        self.evento_tipo = evento_tipo
        self.evento_data = evento_data

        self.text_widget = Text(
            pos=(0, 0),
            texto=texto,
            cor=Colors.TEXT_DARK,
            tamanho=24,
            bold=True,
            centralizar_em_rect=self.rect,
        )

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        abs_rect = self.rect.move(offset)
        pygame.draw.rect(tela, self.cor_fundo, abs_rect, border_radius=5)
        self.text_widget.desenhar(tela, offset)

    def handle_event(
        self, event: pygame.event.Event, offset: tuple[float, float] = (0, 0)
    ):
        if event.type == pygame.MOUSEBUTTONDOWN:
            abs_rect = self.rect.move(offset)
            if abs_rect.collidepoint(event.pos):
                post_evento(self.evento_tipo, **self.evento_data)


class ChoiceButton(Button):
    def __init__(
        self,
        *,
        rect: pygame.Rect,
        texto: str,
        evento_tipo: int,
        id_escolha: str,
        game_state_ro,
        **evento_data,
    ):
        super().__init__(rect=rect, texto=texto, evento_tipo=evento_tipo, **evento_data)
        self.id_escolha = id_escolha
        self.game_state_ro = game_state_ro
        self.cor_sel = Colors.BUTTON_SELECTED

        self.text_widget.fonte = pygame.font.SysFont("Arial", 18, bold=True)

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        selecionado = self.game_state_ro.dificuldade == self.id_escolha
        cor = self.cor_sel if selecionado else self.cor_fundo

        abs_rect = self.rect.move(offset)
        pygame.draw.rect(tela, cor, abs_rect, border_radius=5)
        self.text_widget.desenhar(tela, offset)


class SliderWidget(BaseView):
    def __init__(self, *, x_inicio, x_fim, y, label, game_state_ro):
        self.x_inicio = x_inicio
        self.x_fim = x_fim
        self.y = y
        self.game_state_ro = game_state_ro
        self.knob_radius = 8
        self._arrastando = False

        self.label_widget = Text(
            pos=(x_inicio, y - 35), texto=label, cor=Colors.TEXT_DEFAULT, tamanho=20
        )

    def _obter_knob_pos_abs(self, offset_x):
        largura_total = self.width
        return int(
            offset_x + self.x_inicio + (self.game_state_ro.volume * largura_total)
        )

    @property
    def width(self):
        return self.x_fim - self.x_inicio

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        ox, oy = offset
        self.label_widget.desenhar(tela, offset)

        pygame.draw.line(
            tela,
            Colors.SLIDER_LINE,
            (self.x_inicio + ox, self.y + oy),
            (self.x_fim + ox, self.y + oy),
            3,
        )

        knob_x_abs = self._obter_knob_pos_abs(ox)
        pygame.draw.circle(
            tela, Colors.KNOB_MAIN, (knob_x_abs, self.y + oy), self.knob_radius
        )
        pygame.draw.circle(
            tela, Colors.KNOB_INNER, (knob_x_abs, self.y + oy), self.knob_radius - 2
        )

    def handle_event(
        self, event: pygame.event.Event, offset: tuple[float, float] = (0, 0)
    ):
        ox, oy = offset
        if event.type == pygame.MOUSEBUTTONDOWN:
            knob_x_abs = self._obter_knob_pos_abs(ox)
            dist = (
                (event.pos[0] - knob_x_abs) ** 2 + (event.pos[1] - (self.y + oy)) ** 2
            ) ** 0.5
            if dist <= self.knob_radius + 5:
                self._arrastando = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._arrastando = False
        elif event.type == pygame.MOUSEMOTION and self._arrastando:
            pos_x_local = event.pos[0] - ox
            pos_x_local = max(self.x_inicio, min(pos_x_local, self.x_fim))

            novo_vol = (pos_x_local - self.x_inicio) / self.width
            post_evento(VOLUME_ALTERADO, volume=novo_vol)


class PlacarWidget(BaseView):
    def __init__(self, *, rect: pygame.Rect, game_state_ro):
        self.rect = rect
        self.game_state_ro = game_state_ro

        self.text_widget = Text(
            pos=(0, 0),
            texto="00:00",
            cor=Colors.TEXT_RED,
            tamanho=32,
            bold=True,
            fonte_nome="Consolas",
            centralizar_em_rect=self.rect,
        )

    def _formatar_tempo(self) -> str:
        total_segundos = self.game_state_ro.tempo_segundos
        minutos = total_segundos // 60
        segundos = total_segundos % 60
        return f"{minutos:02}:{segundos:02}"

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        abs_rect = self.rect.move(offset)
        # Fundo do placar
        pygame.draw.rect(tela, Colors.PLACAR_BG, abs_rect)
        pygame.draw.rect(tela, Colors.PANEL_BORDER, abs_rect, 1)

        # Atualiza o texto do widget antes de desenhar
        self.text_widget.texto = self._formatar_tempo()
        self.text_widget.desenhar(tela, offset)


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
