import pygame
from pygame.locals import *


pygame.init()

#tela
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Fase 3')

#cores
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,100,255)
red = (255,0,0)
magenta = (255,0,255)

#chão

ground_height = 50
ground = pygame.Rect(0,screen_height - ground_height, screen_width, ground_height)


#final

final_syze = 100
final = pygame.Rect(screen_width - final_syze, screen_height - ground_height- final_syze, final_syze, final_syze)
passou = False


#enemy
enemy_syze = 40
enemy = pygame.Rect(screen_width - final_syze - enemy_syze, screen_height - ground_height - enemy_syze, enemy_syze, enemy_syze)
morreu = False
enemy_speed = 8
borda_esquerda = 0
borda_direita = screen_width - final_syze - enemy_syze

#personagem

player_size = 50
player = pygame.Rect(0, 0, player_size,player_size)
player.bottomleft = ground.topleft

#gravidade e pulo

y_velocity = 0
gravity = 0.5
is_on_ground = False
jump = -10


#função para o inimigo de mover

def mover():
    global enemy,enemy_speed, borda_direita,borda_esquerda
    enemy.x += enemy_speed

    if enemy.left < borda_esquerda or enemy.left > borda_direita:
        enemy_speed *= -1
    

#função pra reiniciar o jogo

def reiniciar_jogo():
    global player, y_velocity, is_on_ground, passou, morreu, enemy, enemy_speed
    player.x = 0
    player.y = 0
    player.bottomleft = ground.topleft

    enemy.right = screen_width - final_syze
    enemy.bottom = ground.top

    enemy_speed = 8
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

    #mover o inimigo
        mover()

    #colisao com o chao
        if player.colliderect(ground):
            player.bottom = ground.top
            y_velocity = 0
            is_on_ground = True

    #colisao com o inimigo
        if player.colliderect(enemy):
            morreu = True


    #colisao com o final
        if player.colliderect(final):
            passou = True

    #desenhando as parada da tela
        screen.fill(blue)
        pygame.draw.rect(screen,red,player)
        pygame.draw.rect(screen,green,ground)
        pygame.draw.rect(screen,black,final)
        pygame.draw.rect(screen,magenta,enemy)
    elif morreu:
        fonte = pygame.font.SysFont('arial', 20, True, True)
        message = 'Você morreu!!, Pressione R para repetir'
        text= fonte.render(message,True,white)
        screen.fill(red)
        screen.blit(text,(screen_width//2 - text.get_width()//2, screen_height // 2 - text.get_height() // 2))

    elif passou:
        fonte = pygame.font.SysFont('arial',20, True, False)
        message = 'Parabens, você passou de fase!! ' \
        'Pressione R para Repetir.'
        text = fonte.render(message,True,white)

        screen.fill(black)
        screen.blit(text, (screen_width//2 - text.get_width()//2, screen_height //2 - text.get_height() //2))

    
    
    pygame.display.flip()
    clock.tick(60)


pygame.quit()