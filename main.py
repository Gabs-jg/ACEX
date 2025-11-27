import pygame
from game.scenes.level1 import level1
from game import config

def main():
    pygame.init()
    screen = config.create_screen()
    level1(screen)
    pygame.quit()

if __name__ == "__main__":
    main()
