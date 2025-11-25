import pygame

class Inimigo(pygame.Rect):
    # Agora aceitamos 'speed' no __init__ (com padrão 3 se não informar nada)
    def __init__(self, x, y, size, limit_left, limit_right, speed=3):
        super().__init__(x, y, size, size)
        self.color = (255, 0, 255) # Magenta
        
        # Guardamos a velocidade que veio do fase6.py
        self.base_speed = speed 
        self.speed = speed
        
        self.limit_left = limit_left
        self.limit_right = limit_right
        
        self.start_x = x
        self.start_y = y

    def update(self):
        self.x += self.speed

        # Lógica de patrulha inteligente (não treme na parede)
        if self.left <= self.limit_left and self.speed < 0:
            self.speed *= -1
        elif self.right >= self.limit_right and self.speed > 0:
            self.speed *= -1

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        # Reseta para a velocidade base positiva
        self.speed = abs(self.base_speed)

    def draw(self, screen, camera):
        # Como é Fase 6, usa câmera
        rect_visivel = camera.apply(self)
        pygame.draw.rect(screen, self.color, rect_visivel)