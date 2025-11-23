import pygame
from game.scenes.fase1 import fase1
from game import config

def main():
    pygame.init()
    screen = config.create_screen()
    fase1(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
