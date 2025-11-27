import pygame
from game.scenes.level1 import level1
#from game.scenes.fase2 import fase2
from game import config

def main():
    pygame.init()
    screen = config.create_screen()
    level1(screen)
    pygame.quit()
    #fase2(screen)

if __name__ == "__main__":
    main()