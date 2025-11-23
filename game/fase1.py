import pygame
from pygame.locals import *
from .engine import *

def fase1():

    screen = config.create_screen()
    pygame.display.set_caption("Fase 1")

    # Objetos da fase
    ground = create_ground()
    final = create_final()

    player = create_player()

    # Física
    y_velocity = 0
    is_on_ground = False
    passou = False

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not passou:
                if event.type == pygame.KEYDOWN:
                    if (event.key == K_SPACE or event.key == K_w) and is_on_ground:
                        y_velocity = config.JUMP_FORCE
                        is_on_ground = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        # Reinicia fase
                        player.x = config.SCREEN_WIDTH//2 - 25
                        player.y = 0
                        y_velocity = 0
                        is_on_ground = False
                        passou = False

        if not passou:
            keys = pygame.key.get_pressed()

            if keys[K_a]:
                player.x -= 5
            if keys[K_d]:
                player.x += 5

            # Gravidade aplicada
            y_velocity = apply_gravity(player, y_velocity, is_on_ground)

            # Colisão com chão
            y_velocity, is_on_ground = check_ground_collision(player, ground, y_velocity)

            # Chegou ao final da fase
            if player.colliderect(final):
                passou = True

            # Desenho
            screen.fill(config.BLUE)
            pygame.draw.rect(screen, config.RED, player)
            pygame.draw.rect(screen, config.GREEN, ground)
            pygame.draw.rect(screen, config.BLACK, final)

        else:
            screen.fill(config.BLACK)
            draw_text(screen, "Parabéns! Pressione R para repetir.", config.WHITE, 25)

        pygame.display.flip()
        limit_fps()
