import pygame
from .. import config

def create_player():
    return pygame.Rect(config.SCREEN_WIDTH//2 - 25, 0, 50, 50)