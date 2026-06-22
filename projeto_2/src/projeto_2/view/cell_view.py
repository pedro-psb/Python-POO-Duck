import pygame

from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.model.celula import Celula
from projeto_2.view.base_view import BaseView
from projeto_2.view.colors import Colors
from projeto_2.view.widget_views import Text


class CellView(BaseView):
    """View responsável por renderizar uma única célula do mapa."""

    CORES_NUMEROS = {
        1: Colors.NUM_1,
        2: Colors.NUM_2,
        3: Colors.NUM_3,
        4: Colors.NUM_4,
        5: Colors.NUM_5,
        6: Colors.NUM_6,
        7: Colors.NUM_7,
        8: Colors.NUM_8,
    }

    def __init__(
        self,
        celula: Celula,
        spritesheet: pygame.Surface,
        local_offset: tuple[float, float],
        size: int = 32,
    ):
        self.size = size
        self.celula = celula
        self.spritesheet = spritesheet
        self.local_offset = local_offset

        # Widget de texto reutilizável para os números das células
        self._text_widget = Text(
            pos=(0, 0),
            texto="",
            cor=Colors.TEXT_DEFAULT,
            tamanho=22,
            bold=True,
            fonte_nome="Arial",
        )

    def _obter_sprites_sobrepostos(self) -> list[int]:
        """Retorna sprites que não são números (bombas e bandeiras)."""
        sprites = []
        if self.celula.status:  # Escondida
            bandeira = self.celula.obter_entidade(Bandeira)
            if bandeira:
                sprites.append(bandeira.sprite)
        else:  # Revelada
            bomba = self.celula.obter_entidade(Bomba)
            if bomba:
                sprites.append(bomba.sprite)
        return sprites

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        final_x = offset[0] + self.local_offset[0]
        final_y = offset[1] + self.local_offset[1]
        final_pos = (final_x, final_y)

        # 1. Sprite base da célula usando o estado do modelo
        rect_base = pygame.Rect(self.celula.sprite, 0, self.size, self.size)
        tela.blit(self.spritesheet, final_pos, rect_base)

        # 2. Se revelada e com valor, desenha o número
        if not self.celula.status and self.celula.valor > 0:
            self._text_widget.texto = str(self.celula.valor)
            self._text_widget.cor = self.CORES_NUMEROS.get(
                self.celula.valor, Colors.TEXT_DEFAULT
            )
            # Centraliza o texto na célula
            rect_celula = pygame.Rect(
                final_x,
                final_y,
                self.size,
                self.size,
            )
            self._text_widget.centralizar_em_rect = rect_celula
            self._text_widget.desenhar(tela, offset=(0, 0))

        # 3. Desenha outras entidades sobrepostas
        for sprite_x in self._obter_sprites_sobrepostos():
            rect_extra = pygame.Rect(sprite_x, 0, self.size, self.size)
            tela.blit(self.spritesheet, final_pos, rect_extra)
