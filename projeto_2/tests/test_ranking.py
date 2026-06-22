from projeto_2.persistencia.ranking_db import RepositorioRankingJSON


def test_salvar_e_listar_ranking(tmp_path):
    """Testa se o recorde é salvo e se o TOP 10 vem ordenado corretamente."""
    arquivo_teste = tmp_path / "ranking_test.json"
    repo = RepositorioRankingJSON(caminho_arquivo=str(arquivo_teste))

    # 1. Salva alguns recordes bagunçados (tempos diferentes)
    repo.salvar_pontuacao(tempo=45, dificuldade="Medio")
    repo.salvar_pontuacao(tempo=30, dificuldade="Medio")
    repo.salvar_pontuacao(tempo=60, dificuldade="Medio")
    repo.salvar_pontuacao(tempo=20, dificuldade="Facil")  # Dificuldade diferente

    # 2. Busca os melhores da dificuldade "Medio"
    melhores_medio = repo.listar_melhores("Medio")

    # 3. Validações (Asserts)
    assert len(melhores_medio) == 3  # Devem ter 3 registros no Medio

    # O menor tempo (30s) deve vir em primeiro lugar!
    assert melhores_medio[0]["tempo_segundos"] == 30

    # O maior tempo (60s) deve vir por último
    assert melhores_medio[-1]["tempo_segundos"] == 60


def test_limite_top_10(tmp_path):
    """Garante que mesmo com 15 recordes, o repositório só retorna os 10 melhores."""
    arquivo_teste = tmp_path / "ranking_test.json"
    repo = RepositorioRankingJSON(caminho_arquivo=str(arquivo_teste))

    # Salva 12 recordes na mesma dificuldade
    for i in range(1, 13):
        repo.salvar_pontuacao(tempo=100 - i, dificuldade="Dificil")

    melhores_dificil = repo.listar_melhores("Dificil")

    # Deve cortar estritamente no 10
    assert len(melhores_dificil) == 10
