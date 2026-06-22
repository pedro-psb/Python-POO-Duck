import pygame


def post_evento(tipo_evento, **kwargs):
    """Cria e posta um evento customizado no sistema de eventos do Pygame."""
    pygame.event.post(pygame.event.Event(tipo_evento, kwargs))
