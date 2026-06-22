from projeto_2.persistencia.ranking_db import RepositorioRankingJSON

repo = RepositorioRankingJSON("ranking.local.json")

print("--- Inserindo recordes no sistema ---")
repo.salvar_pontuacao(tempo=42, dificuldade="Medio")
repo.salvar_pontuacao(tempo=55, dificuldade="Medio")
repo.salvar_pontuacao(tempo=38, dificuldade="Medio")

print("\n--- Buscando o Top 10 ordenado da dificuldade 'Medio' ---")
top_10 = repo.listar_melhores(dificuldade="Medio")

for posicao, jogador in enumerate(top_10, start=1):
    print(f"{posicao}º Lugar: {jogador['tempo_segundos']}s ({jogador['dificuldade']})")
