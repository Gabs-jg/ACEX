import pygame
from pygame.locals import *


pygame.init()

#tela

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Fase 1')

#cores
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,100,255)
red = (255,0,0)

#chão

ground_height = 50
ground = pygame.Rect(0,screen_height - ground_height, screen_width, ground_height)


#final

final_syze = 100
final = pygame.Rect(screen_width - final_syze, screen_height - ground_height- final_syze, final_syze, final_syze)
passou = False


#personagem

player_size = 50
player = pygame.Rect(screen_width // 2 - player_size // 2, 0, player_size,player_size)

#gravidade e pulo

y_velocity = 0
gravity = 0.5
is_on_ground = False
jump = -10


#função pra reiniciar o jogo

def reiniciar_jogo():
    global player, y_velocity, is_on_ground, passou
    player.x = screen_width //2 - player_size //2
    player.y = 0

    y_velocity = 0
    is_on_ground = False

    passou = False
    


#loop jogo

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not passou:
            if event.type == pygame.KEYDOWN:
                if (event.key == K_SPACE or event.key == K_w) and is_on_ground:
                     y_velocity = jump
                     is_on_ground = False
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    reiniciar_jogo()

    
    if not passou:
    
    #movimento esquerda e direita
        if pygame.key.get_pressed()[K_a]:
            player.x -= 5
        if pygame.key.get_pressed()[K_d]:
            player.x += 5

    #gravidade do personagem
        y_velocity += gravity
        player.y += y_velocity


    #colisao com o chao
        if player.colliderect(ground):
            player.bottom = ground.top
            y_velocity = 0
            is_on_ground = True


    #colisao com o final
        if player.colliderect(final):
            passou = True

    #desenhando as parada da tela
        screen.fill(blue)
        pygame.draw.rect(screen,red,player)
        pygame.draw.rect(screen,green,ground)
        pygame.draw.rect(screen,black,final)

    else:
        fonte = pygame.font.SysFont('arial',20, True, False)
        message = 'Parabens, você passou de fase!! ' \
        'Pressione R para Repetir.'
        text = fonte.render(message,True,white)

        screen.fill(black)
        screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height //2 - text.get_height() //2))

    
    
    pygame.display.flip()
    clock.tick(60)


pygame.quit()