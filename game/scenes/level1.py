import pygame
from pygame.locals import *
from ..engine import *
from ..entities import *
from game.entities.plataform import plataform as pl

def level1 (screen):
    pygame.display.set_caption('Fase 1 - Introdução')
    clock = pygame.time.Clock()

    # 1. Chão
    ground = pl.create_ground()

    # 2. Saída
    final_size = 100
    porta_final = Porta(SCREEN_WIDTH - final_size, SCREEN_HEIGHT - ground_height - final_size, final_size)

    # 3. Player
    player_size = 50
    # Começa no meio da tela (width//2), lá no topo (y=0)
    start_x = SCREEN_WIDTH // 2 - player_size // 2
    player = Player(start_x, 0, player_size, SCREEN_WIDTH)

    # --- Estados ---
    passou = False

    def reiniciar_jogo():
        global passou
        player.reset()
        passou = False

    # --- Loop Principal ---
    running = True
    while running:
        # 1. Checagem de Eventos (Inputs únicos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not passou:
                if event.type == pygame.KEYDOWN:
                    if (event.key == K_SPACE or event.key == K_w):
                        player.jump()
            else:
                if event.type == pygame.KEYDOWN and event.key == K_r:
                    reiniciar_jogo()

        # 2. Atualização da Lógica (Se o jogo não acabou)
        if not passou:
            player.update(ground)

            if player.colliderect(porta_final):
                passou = True

            # 3. Desenho na Tela
            screen.fill(config.BLUE)
            
            ground.draw(screen)
            porta_final.draw(screen)
            player.draw(screen)

        # Tela de Vitória
        elif passou:
            font = pygame.font.SysFont('arial', 20, True, False)
            text = font.render('Parabéns, passou de fase!! Pressione R para Repetir.', True, WHITE)
            screen.fill(config.BLACK)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()       