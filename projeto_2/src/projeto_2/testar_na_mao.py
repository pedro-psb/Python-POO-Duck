from projeto_2.persistencia.ranking_db import RepositorioRankingJSON

repo = RepositorioRankingJSON("ranking.json")

print("--- Inserindo recordes no sistema ---")
repo.salvar_pontuacao(nome="Gui Augusto", tempo=42, dificuldade="Médio")
repo.salvar_pontuacao(nome="Pedro Editor", tempo=55, dificuldade="Médio")
repo.salvar_pontuacao(nome="Emanuelle", tempo=38, dificuldade="Médio")

print("\n--- Buscando o Top 10 ordenado da dificuldade 'Médio' ---")
top_10 = repo.listar_melhores(dificuldade="Médio")

for posicao, jogador in enumerate(top_10, start=1):
    print(
        f"{posicao}º Lugar: {jogador['nome_jogador']} - "
        f"{jogador['tempo_segundos']}s ({jogador['dificuldade']})"
    )
