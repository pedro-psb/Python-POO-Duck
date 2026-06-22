from projeto_2.controller.game_controller import GameController
from projeto_2.model.game_model import GameModel
from projeto_2.model.game_state import GameState
from projeto_2.model.mapa_quadrado import MapaQuadrado
from projeto_2.view.game_view import GameView


def run():
    largura, altura = 800, 600
    game_state = GameState()
    mapa = MapaQuadrado(18, 18, total_bombas=game_state.qtd_bombas)
    game_model = GameModel(mapa, game_state)

    view = GameView(game_model, largura, altura)
    controller = GameController(view, game_model)
    controller.run()


if __name__ == "__main__":
    run()
