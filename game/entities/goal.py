import pygame
from game import config


class Goal:
    def __init__(self, x, y, width, height, color=(255, 215, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    @staticmethod
    def create_goal(ground=None):
        # Tamanho do quadrado
        goal_width = 100
        goal_height = 100

        # Posição horizontal (mais à direita, ajustável)
        # Eu também não sei por que mas 100 em altura e largura ficou bom
        x = config.SCREEN_WIDTH - 100
        y = config.SCREEN_HEIGHT + 100

        # Se recebeu o chão → alinha exatamente no topo do chão
        if ground is not None:
            y = ground.rect.top - goal_height
        else:
            # fallback (não recomendado)
            # Esse -80 é pro quadrado não "nascer" em por cima do chão, mas nascer exatamente em cima dele.
            y = config.SCREEN_HEIGHT - goal_height - 80

        return Goal(x, y, goal_width, goal_height)
