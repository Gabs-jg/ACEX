import pygame
from pygame.locals import *
from ..entities.objects import *
from ..entities.player import *
from pygame.locals import *
from ..engine import *


def fase2(screen):
    pygame.display.set_caption('Fase 2')

    ground_height = 50
    ground = create_ground()
    goal = create_goal()
    player = create_player

    #buraco

    hole_radius = 20
    hole = pygame.Rect(0,0,hole_radius * 2, hole_radius *2)
    hole.centerx = config.SCREEN_WIDTH // 2
    hole.bottom = ground.top
    morreu = False

    #personagem

    player_size = 50
    player = pygame.Rect(0, 0, player_size,player_size)
    player.bottomleft = ground.topleft

    #gravidade e pulo

    y_velocity = 0
    gravity = 0.5
    is_on_ground = False
    jump = -10


    passou = False
    #função pra reiniciar o jogo

    def reiniciar_jogo():
        global player, y_velocity, is_on_ground, passou, morreu
        player.x = 0
        player.y = 0
        player.bottomleft = ground.topleft

        y_velocity = 0
        is_on_ground = False

        passou = False
        morreu = False
        
        
    #loop jogo
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not passou and not morreu:
                if event.type == pygame.KEYDOWN:
                    if (event.key == K_SPACE or event.key == K_w) and is_on_ground:
                        y_velocity = jump
                        is_on_ground = False
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == K_r:
                        reiniciar_jogo()

        
        if not passou and not morreu:
        
        #movimento esquerda e direita
            if pygame.key.get_pressed()[K_a]:
                player.x -= 5
            if pygame.key.get_pressed()[K_d]:
                player.x += 5

        #gravidade do personagem
            y_velocity += gravity
            player.y += y_velocity


        #colisao com o buraco
            if player.colliderect(hole):
                morreu = True


        #colisao com o chao
            if player.colliderect(ground):
                player.bottom = ground.top
                y_velocity = 0
                is_on_ground = True


        #colisao com o final
            if player.colliderect(goal):
                passou = True

        #desenhando as parada da tela
            screen.fill(config.BLUE)
            pygame.draw.rect(screen,config.RED,player)
            pygame.draw.rect(screen,config.GREEN,ground)
            pygame.draw.rect(screen,config.BLACK,goal)
            pygame.draw.circle(screen,config.BLACK,hole.center,hole_radius)
        
        elif morreu:
            fonte = pygame.font.SysFont('arial', 20, True, True)
            message = 'Você morreu!!, Pressione R para repetir'
            text= fonte.render(message,True,config.WHITE)
            screen.fill(config.RED)
            screen.blit(text,(config.SCREEN_WIDTH//2 - text.get_width()//2, config.SCREEN_HEIGHT // 2 - text.get_height() // 2))


        elif passou:
            fonte = pygame.font.SysFont('arial',20, True, False)
            message = 'Parabens, você passou de fase!! ' \
            'Pressione R para Repetir.'
            text = fonte.render(message,True,config.WHITE)

            screen.fill(config.BLACK)
            screen.blit(text, (config.SCREEN_WIDTH//2 - text.get_width()//2, config.SCREEN_HEIGHT //2 - text.get_height() //2))

        
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()