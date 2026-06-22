import pygame

from projeto_2.constants import CELULA_CLICK
from projeto_2.utils import post_evento

from .base_view import BaseView
from .cell_view import CellView


class MapaView(BaseView):
    def __init__(
        self,
        *,
        mapa_ro,
        spritesheet,
        area: tuple[int, int],
        tamanho_celula: int = 32,
    ):
        self.mapa_ro = mapa_ro
        self.spritesheet = spritesheet
        self.area = area
        self.tamanho_celula = tamanho_celula
        self.local_offset = (0, 0)
        self._init_cell_views()

    def _init_cell_views(self):
        """Inicializa a matriz de CellViews para cada célula do mapa."""
        self._cell_views = [
            [
                CellView(
                    self.mapa_ro.obter_celula(x, y),
                    self.spritesheet,
                    local_offset=(x * self.tamanho_celula, y * self.tamanho_celula),
                    size=self.tamanho_celula,
                )
                for x in range(self.mapa_ro.colunas)
            ]
            for y in range(self.mapa_ro.linhas)
        ]

    def _atualizar_offsets(self):
        """Calcula a centralização do mapa baseada na área disponível."""
        offset_x = (self.area[0] - (self.mapa_ro.colunas * self.tamanho_celula)) // 2
        offset_y = (self.area[1] - (self.mapa_ro.linhas * self.tamanho_celula)) // 2
        self.local_offset = (offset_x, offset_y)

    def _converter_tela_para_grade(self, pos, parent_offset=(0, 0)):
        """Converte coordenadas da tela para (x, y) da grade, considerando offsets."""
        self._atualizar_offsets()
        ox, oy = parent_offset
        px, py = pos
        gx = (px - (ox + self.local_offset[0])) // self.tamanho_celula
        gy = (py - (oy + self.local_offset[1])) // self.tamanho_celula
        return int(gx), int(gy)

    def handle_event(self, event, offset: tuple[float, float] = (0, 0)):
        if event.type == pygame.MOUSEBUTTONDOWN:
            grid_pos = self._converter_tela_para_grade(event.pos, offset)
            gx, gy = grid_pos
            if 0 <= gx < self.mapa_ro.colunas and 0 <= gy < self.mapa_ro.linhas:
                post_evento(CELULA_CLICK, pos=grid_pos, button=event.button)

    def desenhar(self, tela: pygame.Surface, offset: tuple[float, float] = (0, 0)):
        self._atualizar_offsets()

        # Verifica se o mapa foi resetado checando a referência da primeira célula
        primeira_celula = self.mapa_ro.obter_celula(0, 0)
        if primeira_celula and self._cell_views[0][0].celula is not primeira_celula:
            self._init_cell_views()

        ox, oy = offset
        ax = ox + self.local_offset[0]
        ay = oy + self.local_offset[1]
        parent_offset = (ax, ay)

        for y in range(self.mapa_ro.linhas):
            for x in range(self.mapa_ro.colunas):
                cell_view = self._cell_views[y][x]
                cell_view.desenhar(tela, offset=parent_offset)
