import pygame

from projeto_2.constants import FECHAR_RANKING
from projeto_2.persistencia.ranking_db import RepositorioRankingJSON
from projeto_2.view.colors import Colors
from projeto_2.view.widget_views import Button, PopupView, Text


class GameRankingView(PopupView):
    """View do ranking refatorada para usar PopupView."""

    def __init__(self, *, area: tuple[int, int]):
        self.repo = RepositorioRankingJSON("ranking.local.json")

        # Definição dos widgets estáticos
        self.label_titulo = Text(
            pos=(0, 0),
            texto="RECORDES - TOP 10",
            cor=Colors.BUTTON_SELECTED,
            tamanho=32,
            bold=True,
            centralizar_em_rect=pygame.Rect(0, 20, 450, 40),
        )
        self.label_subtitulo = Text(
            pos=(0, 0),
            texto="Dificuldade",
            cor=Colors.WHITE,
            tamanho=18,
            bold=False,
            centralizar_em_rect=pygame.Rect(0, 60, 450, 30),
        )
        self.btn_voltar = Button(
            rect=pygame.Rect(150, 450, 150, 40),
            texto="VOLTAR",
            evento_tipo=FECHAR_RANKING,
        )

        self.record_widgets = []

        # Inicializa o PopupView com os widgets estáticos inicialmente
        super().__init__(
            area=area,
            widgets=[self.label_titulo, self.label_subtitulo, self.btn_voltar],
            largura_box=450,
            altura_box=520,
        )

    def atualizar_dificuldade(self, dificuldade_atual: str):
        """Atualiza a dificuldade exibida e reconstrói a lista de recordes."""
        self.label_subtitulo.texto = f"Dificuldade: {dificuldade_atual.upper()}"

        melhores = self.repo.listar_melhores(dificuldade_atual)
        self.record_widgets = []

        pos_y = 110
        if not melhores:
            self.record_widgets.append(
                Text(
                    pos=(0, 0),
                    texto="Nenhum recorde nesta dificuldade!",
                    cor=Colors.TEXT_DEFAULT,
                    tamanho=18,
                    bold=False,
                    centralizar_em_rect=pygame.Rect(0, pos_y + 80, 450, 30),
                )
            )
        else:
            for indice, registro in enumerate(melhores, start=1):
                tempo = registro["tempo_segundos"]

                left_text = f"{indice}º Lugar"
                right_text = f"{tempo}s"

                self.record_widgets.append(
                    Text(
                        pos=(50, pos_y),
                        texto=left_text,
                        cor=Colors.WHITE,
                        tamanho=20,
                        bold=False,
                    )
                )
                self.record_widgets.append(
                    Text(
                        pos=(350, pos_y),
                        texto=right_text,
                        cor=Colors.WHITE,
                        tamanho=20,
                        bold=True,
                    )
                )
                pos_y += 32

        # Atualiza a lista completa de widgets do PopupView
        self.widgets = [
            self.label_titulo,
            self.label_subtitulo,
            self.btn_voltar,
        ] + self.record_widgets
