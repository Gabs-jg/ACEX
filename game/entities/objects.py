import pygame
from .. import config

def create_ground():
    ground_height=50
    return pygame.Rect(0, config.SCREEN_HEIGHT - ground_height, config.SCREEN_WIDTH, ground_height)

def create_goal():
    return pygame.Rect(config.SCREEN_WIDTH - 100, config.SCREEN_HEIGHT - 150, 100, 100)



