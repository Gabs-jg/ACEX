import pygame
from pygame.locals import *

from game import config
from game.entities.player import Player
from game.entities.plataform import Plataform
from game.entities.goal import Goal


def level1(screen):
    pygame.display.set_caption("Fase 1 - Introdução")
    clock = pygame.time.Clock()

    # ----- BACKGROUND -----
    background = pygame.image.load("game/assets/images/background.png").convert()
    background = pygame.transform.scale(background, (config.SCREEN_WIDTH, config.SCREEN_HEIGHT))

    # ----- OBJETOS DA CENA -----
    ground = Plataform.create_ground()
    platforms = [ground]  # lista de plataformas

    goal = Goal.create_goal()

    # ----- PLAYER -----
    # Eu não sei por que mas 37 (em player_size) é o número que fica aceitável pro personagem encostar no chão.
    # Então não mexa se não saber o que ta fazendo.
    player_size = 37  
    start_x = config.SCREEN_WIDTH // 2 - config.SCREEN_HEIGHT // 2
    player = Player(start_x, 0, player_size, config.SCREEN_WIDTH)

    passou = False

    # ----- FUNÇÃO PARA REINICIAR -----
    def reiniciar():
        nonlocal passou
        player.reset(start_x, 0)
        passou = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Controles
            if not passou:
                if event.type == pygame.KEYDOWN:
                    if event.key in (K_SPACE, K_w):
                        player.jump()

            else:
                if event.type == pygame.KEYDOWN and event.key == K_r:
                    reiniciar()

        # ----- UPDATE -----
        if not passou:
            player.update(platforms)

            # Verificar chegada no objetivo
            if player.colliderect(goal):
                passou = True

            # ----- DESENHAR -----
            screen.blit(background, (0, 0))

            for plat in platforms:
                plat.draw(screen)

            goal.draw(screen)
            player.draw(screen)

        # ----- TELA DE VITÓRIA -----
        else:
            screen.fill(config.BLACK)
            font = pygame.font.SysFont("arial", 26, True)

            msg = "Parabéns! Aperte R para reiniciar."
            text = font.render(msg, True, config.WHITE)

            screen.blit(
                text,
                (config.SCREEN_WIDTH // 2 - text.get_width() // 2,
                 config.SCREEN_HEIGHT // 2)
            )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
