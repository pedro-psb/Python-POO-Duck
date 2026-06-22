import pygame

from projeto_2.controller.mapa_controller import MapaController
from projeto_2.model.bandeira import Bandeira
from projeto_2.model.bomba import Bomba
from projeto_2.model.game_state import GameState
from projeto_2.model.mapa_quadrado import MapaQuadrado
from projeto_2.persistencia.ranking_db import RepositorioRankingJSON
from projeto_2.view.mapa_view import MapaView


def test_mapa_view_converter_tela_para_grade_sem_offset():
    """Testa a conversão de coordenadas da tela para a grade (sem offset adicional)."""
    pygame.init()
    mapa = MapaQuadrado(linhas=10, colunas=10, total_bombas=10)
    view = MapaView(
        mapa_ro=mapa,
        spritesheet=pygame.Surface((10, 10)),
        area=(320, 320),  # Mapa 320x320 se encaixa perfeitamente
        tamanho_celula=32,
    )

    assert view._converter_tela_para_grade((0, 0)) == (0, 0)
    assert view._converter_tela_para_grade((31, 31)) == (0, 0)
    assert view._converter_tela_para_grade((32, 32)) == (1, 1)


def test_mapa_view_converter_tela_para_grade_com_offset():
    """Testa a conversão de coordenadas considerando a centralização do MapaView."""
    pygame.init()
    mapa = MapaQuadrado(linhas=10, colunas=10, total_bombas=10)
    # Área de 400x400 para um mapa de 320x320 gera um offset de (40, 40)
    view = MapaView(
        mapa_ro=mapa,
        spritesheet=pygame.Surface((10, 10)),
        area=(400, 400),
        tamanho_celula=32,
    )

    off_x, off_y = (0, 0)  # parent offset simulado

    assert view._converter_tela_para_grade(
        (100, 100), parent_offset=(off_x, off_y)
    ) == (
        1,
        1,
    )  # 100 - 40 = 60 // 32 = 1
    assert view._converter_tela_para_grade(
        (131, 131), parent_offset=(off_x, off_y)
    ) == (
        2,
        2,
    )  # 131 - 40 = 91 // 32 = 2
    assert view._converter_tela_para_grade(
        (132, 132), parent_offset=(off_x, off_y)
    ) == (
        2,
        2,
    )  # 132 - 40 = 92 // 32 = 2


def test_mapa_controller_game_over():
    """Garante que atingir uma bomba finaliza o jogo e revela o mapa."""
    game_state = GameState()
    mapa = MapaQuadrado(3, 3, total_bombas=1)
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
    mapa = MapaQuadrado(3, 3, total_bombas=1)
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


def test_mapa_controller_victory(monkeypatch):
    """Garante que revelar células seguras declara vitória e salva ranking."""
    game_state = GameState()
    game_state.qtd_bombas = 1
    mapa = MapaQuadrado(2, 2, total_bombas=1)
    controller = MapaController(game_state, mapa)

    # Place a single bomb at (1, 1)
    bomba = Bomba(1, False, 0)
    mapa.obter_celula(1, 1).adicionar_bomba(bomba)
    mapa.contar_bombas_vizinhas()

    # Track calls to salvar_pontuacao
    salvas = []

    monkeypatch.setattr(
        RepositorioRankingJSON,
        "salvar_pontuacao",
        lambda self, tempo, dificuldade: salvas.append((tempo, dificuldade)),
    )

    # Simulate clicks on safe cells
    game_state.primeiro_clique = False

    # Click all safe cells: (0,0), (0,1), (1,0)
    controller.handle_clique_esquerdo(0, 0)
    controller.handle_clique_esquerdo(0, 1)
    controller.handle_clique_esquerdo(1, 0)

    # Hidden cells should only be the bomb at (1,1) (1 hidden cell)
    # Since game_state.qtd_bombas is 1, this should trigger win!
    assert game_state.jogo_finalizado is True
    assert len(salvas) == 1
    assert salvas[0][1] == game_state.dificuldade


def test_mapa_total_bombas_validation():
    """Garante que a quantidade de bombas deve ser um inteiro positivo."""
    mapa = MapaQuadrado(5, 5, total_bombas=5)

    # Validações bem sucedidas
    mapa.total_bombas = 5
    assert mapa.total_bombas == 5

    # Inteiro não positivo deve lançar ValueError
    import pytest

    with pytest.raises(ValueError):
        mapa.total_bombas = 0

    with pytest.raises(ValueError):
        mapa.total_bombas = -1

    # Tipo incorreto deve lançar ValueError
    with pytest.raises(ValueError):
        mapa.total_bombas = "cinco"  # type: ignore
