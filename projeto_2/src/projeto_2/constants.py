import pygame

# Eventos Customizados do Jogo
# Usamos pygame.USEREVENT como base para evitar conflitos com eventos do sistema
CELULA_CLICK = pygame.USEREVENT + 1
REINICIAR_CLICK = pygame.USEREVENT + 2
PLACAR_CLICK = pygame.USEREVENT + 3
DIFICULDADE_ALTERADA = pygame.USEREVENT + 4
VOLUME_ALTERADO = pygame.USEREVENT + 5
PAUSA_TOGGLE = pygame.USEREVENT + 6
FECHAR_RANKING = pygame.USEREVENT + 7
FECHAR_VITORIA = pygame.USEREVENT + 8

# Configurações de Áudio
VOLUME_MAX = 0.3
