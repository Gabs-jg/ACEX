import pygame

# Tamanho da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Cores básicas
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,100,255)
RED = (255,0,0)

# Gravidade e física
GRAVITY = 0.5
JUMP_FORCE = -10

# Criação da tela
def create_screen():
    return pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 