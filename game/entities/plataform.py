import pygame
from . import config

class plataform(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, screen):
        # Desenha direto na tela
        pygame.draw.rect(screen, self.color, self)

    def create_ground():
        ground_height=50
        return pygame.Rect(0, config.SCREEN_HEIGHT - ground_height, config.SCREEN_WIDTH, ground_height)