import pygame

class Espinho(pygame.Rect):
    def __init__(self, x, y, width):
        # Espinhos são baixinhos (height=10) e ficam no chão
        super().__init__(x, y, width, 10)
        self.color = (255, 50, 50) # Vermelho Perigo

    def draw(self, screen, camera):
        rect_visivel = camera.apply(self)
        pygame.draw.rect(screen, self.color, rect_visivel)