import pygame
from game import config

class Plataform:
    def __init__(self, x, y, width, height, color=(0, 200, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    @staticmethod
    def create_ground():
        ground_height = 80
        return Plataform(
            0,
            config.SCREEN_HEIGHT - ground_height,
            config.SCREEN_WIDTH,
            ground_height
        )
