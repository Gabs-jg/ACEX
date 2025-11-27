import pygame
from game import config

clock = pygame.time.Clock()

#Functions
def apply_gravity(player_rect, y_velocity, is_on_ground):
    if not is_on_ground:
        y_velocity += config.GRAVITY
        player_rect.y += y_velocity
    return y_velocity

def check_ground_collision(player_rect, ground_rect, y_velocity):
    if player_rect.colliderect(ground_rect):
        player_rect.bottom = ground_rect.top
        return 0, True
    return y_velocity, False

def draw_text(screen, message, color=config.WHITE, size=30):
    font = pygame.font.SysFont('arial', size, True)
    text = font.render(message, True, color)
    x = config.SCREEN_WIDTH // 2 - text.get_width() // 2
    y = config.SCREEN_HEIGHT // 2 - text.get_height() // 2
    screen.blit(text, (x, y))

def limit_fps():
    clock.tick(60)