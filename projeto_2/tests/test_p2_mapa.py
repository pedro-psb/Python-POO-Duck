from projeto_2.model.bomba import Bomba
from projeto_2.model.celula import Celula
from projeto_2.model.mapa import Mapa
from projeto_2.model.mapa_quadrado import MapaQuadrado


def test_mapa_quadrado_subclasse_de_mapa():
    """Garante que MapaQuadrado herda da classe abstrata Mapa."""
    assert issubclass(MapaQuadrado, Mapa)


def test_mapa_quadrado_geracao_dimensoes():
    """Garante que o mapa gera a matriz com as dimensões corretas."""
    colunas = 5
    linhas = 3
    mapa_obj = MapaQuadrado(colunas, linhas, total_bombas=1)

    assert len(mapa_obj.mapa) == linhas
    assert len(mapa_obj.mapa[0]) == colunas
    assert mapa_obj.colunas == colunas
    assert mapa_obj.linhas == linhas


def test_mapa_quadrado_conteudo_celulas():
    """Garante que o mapa contém instâncias únicas de Celula e endereços corretos."""
    colunas = 3
    linhas = 3
    mapa_obj = MapaQuadrado(colunas, linhas, total_bombas=1)

    celula_0_0 = mapa_obj.obter_celula(0, 0)
    celula_1_0 = mapa_obj.obter_celula(1, 0)

    assert isinstance(celula_0_0, Celula)
    assert isinstance(celula_1_0, Celula)
    assert celula_0_0 is not celula_1_0

    assert celula_0_0.address == 0
    assert mapa_obj.obter_celula(1, 1).address == 4

    # Verifica status inicial invertido (True = escondida)
    assert celula_0_0.status is True


def test_mapa_quadrado_contar_bombas_vizinhas():
    """Garante que o cálculo de bombas vizinhas está correto."""
    mapa_obj = MapaQuadrado(3, 3, total_bombas=2)

    # Coloca bombas em (0,0) e (1,0)
    mapa_obj.obter_celula(0, 0).adicionar_bomba(Bomba(1, False, 0))
    mapa_obj.obter_celula(1, 0).adicionar_bomba(Bomba(2, False, 0))

    mapa_obj.contar_bombas_vizinhas()

    # Célula (0,1) deve ter 2 bombas vizinhas
    assert mapa_obj.obter_celula(0, 1).valor == 2

    # Célula (2,0) deve ter 1 bomba vizinha
    assert mapa_obj.obter_celula(2, 0).valor == 1

    # Célula (2,2) deve ter 0 bombas vizinhas
    assert mapa_obj.obter_celula(2, 2).valor == 0


def test_mapa_quadrado_revelar_bomba():
    """Garante que revelar uma bomba retorna True."""
    mapa_obj = MapaQuadrado(3, 3, total_bombas=1)
    mapa_obj.obter_celula(1, 1).adicionar_bomba(Bomba(1, False, 0))

    resultado = mapa_obj.revelar(1, 1)
    assert resultado is True
    assert mapa_obj.obter_celula(1, 1).status is False


def test_mapa_quadrado_revelar_seguro():
    """Garante que revelar uma célula sem bomba retorna False."""
    mapa_obj = MapaQuadrado(3, 3, total_bombas=1)
    # Coloca bomba longe
    mapa_obj.obter_celula(0, 0).adicionar_bomba(Bomba(1, False, 0))

    resultado = mapa_obj.revelar(2, 2)
    assert resultado is False


def test_mapa_quadrado_revelar_recursivo():
    """Garante que revelar uma célula com valor 0 revela os vizinhos recursivamente."""
    mapa_obj = MapaQuadrado(3, 3, total_bombas=1)
    mapa_obj.obter_celula(0, 0).adicionar_bomba(Bomba(1, False, 0))
    mapa_obj.contar_bombas_vizinhas()

    # Revelar (2,2) que tem valor 0
    resultado = mapa_obj.revelar(2, 2)

    assert resultado is False
    assert mapa_obj.obter_celula(2, 2).status is False
    assert mapa_obj.obter_celula(0, 0).status is True  # Bomba continua escondida
    assert mapa_obj.obter_celula(1, 0).status is False  # Vizinho de 0 revelado
    assert mapa_obj.obter_celula(0, 1).status is False  # Vizinho de 0 revelado


def test_mapa_quadrado_obter_celula_fora_limite():
    """Garante que retornar None ao acesso fora dos limites."""
    mapa_obj = MapaQuadrado(3, 3, total_bombas=1)
    assert mapa_obj.obter_celula(3, 3) is None
    assert mapa_obj.obter_celula(-1, 0) is None


def test_celula_com_bomba_nao_tem_valor():
    """Garante que células que contêm bombas não possuem valor numérico (valor = 0)."""
    mapa_obj = MapaQuadrado(3, 3, total_bombas=2)
    mapa_obj.obter_celula(0, 0).adicionar_bomba(Bomba(1, False, 0))
    mapa_obj.obter_celula(1, 0).adicionar_bomba(Bomba(2, False, 0))

    mapa_obj.contar_bombas_vizinhas()

    assert mapa_obj.obter_celula(0, 0).valor == 0
    assert mapa_obj.obter_celula(1, 0).valor == 0
    assert mapa_obj.obter_celula(0, 1).valor == 2


def test_mapa_quadrado_distribuir_bombas_seguro():
    """A distribuição de bombas deve respeitar a área segura do primeiro clique."""
    col, lin = 10, 10
    mapa_obj = MapaQuadrado(col, lin, total_bombas=80)

    # Clique em (5,5). A área (4-6, 4-6) deve estar limpa.
    cx, cy = 5, 5
    mapa_obj.distribuir_bombas(cx, cy)  # Muitas bombas para testar o limite

    # Verifica área 3x3 ao redor do clique
    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            celula = mapa_obj.obter_celula(cx + dx, cy + dy)
            assert celula.obter_entidade(Bomba) is None, (
                f"Bomba encontrada em área segura ({cx + dx}, {cy + dy})"
            )
