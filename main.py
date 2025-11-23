import pygame
from game.scenes.fase1 import fase1
from game.scenes.fase2 import fase2
from game import config

def main():
    pygame.init()
    screen = config.create_screen()
    fase1(screen)
    pygame.quit()
    fase2(screen)

if __name__ == "__main__":
    main()
