import pygame

from projeto_2.controller.mapa_controller import MapaController
from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.model.game_state import GameState
from projeto_2.model.mapa_quadrado import MapaQuadrado
from projeto_2.view.mapa_view import MapaView


def test_mapa_view_converter_tela_para_grade_sem_offset():
    """Garante que a conversão de pixels para grid está correta sem offset."""
    pygame.init()
    mapa = MapaQuadrado(10, 10)
    # Area de tamanho exato para que local_offset seja (0, 0)
    view = MapaView(mapa_ro=mapa, spritesheet=None, area=(320, 320))

    assert view.converter_tela_para_grade((0, 0)) == (0, 0)
    assert view.converter_tela_para_grade((31, 31)) == (0, 0)
    assert view.converter_tela_para_grade((32, 32)) == (1, 1)


def test_mapa_view_converter_tela_para_grade_com_offset():
    """A conversão de pixels para grid deve respeitar os offsets."""
    pygame.init()
    mapa = MapaQuadrado(10, 10)
    # Area de tamanho exato para que local_offset seja (0, 0)
    view = MapaView(mapa_ro=mapa, spritesheet=None, area=(320, 320))

    off_x, off_y = 100, 100
    assert view.converter_tela_para_grade((100, 100), parent_offset=(off_x, off_y)) == (
        0,
        0,
    )
    assert view.converter_tela_para_grade((131, 131), parent_offset=(off_x, off_y)) == (
        0,
        0,
    )
    assert view.converter_tela_para_grade((132, 132), parent_offset=(off_x, off_y)) == (
        1,
        1,
    )


def test_mapa_controller_game_over():
    """Garante que atingir uma bomba finaliza o jogo e revela o mapa."""
    game_state = GameState()
    mapa = MapaQuadrado(3, 3)
    controller = MapaController(game_state, mapa)

    # Coloca uma bomba em (1,1)
    bomba = Bomba(1, False, 0)
    mapa.obter_celula(1, 1).adicionar_bomba(bomba)

    # Simula clique esquerdo na bomba
    game_state.primeiro_clique = False
    controller.handle_clique_esquerdo(1, 1)

    assert game_state.jogo_finalizado is True
    # Todas as células devem estar cavadas (status False)
    for linha in mapa.mapa:
        for celula in linha:
            assert celula.status is False

    # A bomba clicada deve estar explodida (sprite index 3 * tamanho_celula = 96)
    assert mapa.obter_celula(1, 1).obter_entidade(Bomba).sprite == 96


def test_mapa_controller_bandeira():
    """Garante que o clique com botão direito adiciona/remove bandeiras."""
    game_state = GameState()
    mapa = MapaQuadrado(3, 3)
    controller = MapaController(game_state, mapa)

    # Inicialmente sem bandeira
    celula = mapa.obter_celula(1, 1)
    assert celula.obter_entidade(Bandeira) is None

    # Adiciona bandeira
    controller.handle_clique_direito(1, 1)
    assert celula.obter_entidade(Bandeira) is not None

    # Remove bandeira
    controller.handle_clique_direito(1, 1)
    assert celula.obter_entidade(Bandeira) is None
