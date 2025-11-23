import pygame
from pygame.locals import *

pygame.init()

#telas
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Fase 4')

#cores
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,100,255)
red = (255,0,0)
magenta = (255,0,255)
yellow = (255, 255, 0) # Cor para as novas plataformas

#chão

ground_height = 50
ground = pygame.Rect(0,screen_height - ground_height, screen_width, ground_height)

# PLATAFORMAS (Novo)
plataformas = [
    pygame.Rect(150, screen_height - ground_height - 100, 200, 20),
    pygame.Rect(400, screen_height - ground_height - 200, 150, 20),
    pygame.Rect(650, screen_height - ground_height - 300, 200, 20)
]

#final

final_syze = 100
final = pygame.Rect(screen_width - final_syze, screen_height - ground_height - final_syze, final_syze, final_syze)
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
# VARIÁVEIS PARA DOUBLE JUMP
max_jumps = 2  # Total de saltos (1 normal + 1 duplo = 2)
jumps_left = max_jumps


# Variáveis para a nova mecânica de DASH
dash_speed = 100 
is_dashing = False
dash_direction = 1 
can_dash = True 

# Variável para rastrear a direção do personagem para o dash
player_direction = 1 

# --- parâmetros de escalada ---
climb_speed = 4    # quanto sobe por frame ao escalar
side_touch_buffer = 5  # margem para detectar toque lateral sem conflitar com topo

#função para o inimigo de mover

def mover():
    global enemy,enemy_speed, borda_direita,borda_esquerda
    enemy.x += enemy_speed

    if enemy.left < borda_esquerda or enemy.left > borda_direita:
        enemy_speed *= -1
    

# Função para detectar toque lateral em plataformas (para escalada)
def touching_platform_side():
    global player
    for platform in plataformas:
        if player.colliderect(platform):
            # assegura que não seja toque por cima/embaixo com buffer
            vertical_overlap = (player.bottom > platform.top + side_touch_buffer) and (player.top < platform.bottom - side_touch_buffer)
            if vertical_overlap:
                # Encostando pela esquerda (player à esquerda da plataforma)
                if player.right > platform.left and player.left < platform.left:
                    return "left"
                # Encostando pela direita (player à direita da plataforma)
                if player.left < platform.right and player.right > platform.right:
                    return "right"
    return None


# Função para colisões horizontais (evita "grudar" e atravessar)
def check_horizontal_collision(dx):
    global player
    if dx == 0:
        return
    player.x += dx
    # checar colisão com plataformas após mover horizontalmente
    for platform in plataformas:
        if player.colliderect(platform):
            # somente trata colisão lateral (quando não está sobre a plataforma)
            if player.bottom > platform.top + 5 and player.top < platform.bottom - 5:
                if dx > 0:
                    player.right = platform.left
                elif dx < 0:
                    player.left = platform.right
    # manter dentro da tela
    player.left = max(0, player.left)
    player.right = min(screen_width, player.right)


# Função para verificar colisão com plataformas (FIXADO CONTRA TUNNELING)
def check_platform_collision():
    global player, y_velocity, is_on_ground, jumps_left
    
    on_platform = False
    
    # salvamos a posição anterior do bottom para anti-tunneling
    prev_bottom = player.bottom - y_velocity

    # Colisão com plataformas: verificar pouso por cima e bater a cabeça por baixo
    for platform in plataformas:
        if player.colliderect(platform):
            # Pouso por cima: estava acima no frame anterior e agora colidiu caindo
            if prev_bottom <= platform.top and player.bottom >= platform.top and y_velocity >= 0:
                player.bottom = platform.top
                y_velocity = 0
                is_on_ground = True
                on_platform = True
                jumps_left = max_jumps
            # Bateu a cabeça embaixo da plataforma ao subir
            elif prev_bottom >= platform.bottom and player.top <= platform.bottom and y_velocity < 0:
                player.top = platform.bottom
                y_velocity = 0
            else:
                # Caso de colisão ambígua (p.ex. teletransporte), empurre para fora verticalmente
                # Se o centro do player está acima do centro da plataforma, coloque em cima; senão coloque em baixo.
                if player.centery < platform.centery:
                    player.bottom = platform.top
                    y_velocity = 0
                    is_on_ground = True
                    on_platform = True
                    jumps_left = max_jumps
                else:
                    player.top = platform.bottom
                    y_velocity = 0

    # Colisão com o chão
    if player.colliderect(ground):
        player.bottom = ground.top
        y_velocity = 0
        is_on_ground = True
        on_platform = True
        jumps_left = max_jumps

    if not on_platform:
        is_on_ground = False


#função pra reiniciar o jogo

def reiniciar_jogo():
    global player, y_velocity, is_on_ground, passou, morreu, enemy, enemy_speed, player_direction, is_dashing, can_dash, jumps_left
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
    
    is_dashing = False 
    can_dash = True
    player_direction = 1
    jumps_left = max_jumps # Resetar o double jump
    

#loop jogo

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not passou and not morreu:
            if event.type == pygame.KEYDOWN:
                # LÓGICA DO SALTO (DOUBLE JUMP)
                if (event.key == K_SPACE or event.key == K_w) and jumps_left > 0:
                    y_velocity = jump
                    jumps_left -= 1
                    is_on_ground = False # O salto sempre tira o personagem do chão

                
                # DASH (Avanço) com a tecla 'E'
                if event.key == K_e and can_dash and not is_dashing:
                    is_dashing = True
                    # can_dash = False 
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    reiniciar_jogo()

    
    if not passou and not morreu:
    
        #movimento esquerda e direita
        keys = pygame.key.get_pressed()
        
        dx = 0
        if keys[K_a]:
            dx = -5
            player_direction = -1 
        if keys[K_d]:
            dx = 5
            player_direction = 1 
            
        # Lógica do DASH (Avanço)
        if is_dashing:
            dx = dash_speed * player_direction
            is_dashing = False 
            # após dash, asseguramos limites na aplicação de check_horizontal_collision

        # Aplicar movimentação horizontal com checagem de colisão
        check_horizontal_collision(dx)

        # gravidade do personagem (aplicada a y_velocity)
        y_velocity += gravity

        # Aplicamos movimento vertical *antes* de checar colisões para calcular prev_bottom corretamente.
        # Contudo, em nossa checagem usamos prev_bottom = player.bottom - y_velocity para anti-tunneling.
        player.y += y_velocity

        # Verifica e corrige colisões verticais (pouso, cabeça)
        check_platform_collision()

        # MECÂNICA: ESCALAR QUANDO ESTÁ ENCOSTANDO LATERALMENTE
        lado = touching_platform_side()
        # se estiver encostando na lateral e pressionar W, sobe (e cancela a queda)
        if lado is not None and keys[K_w]:
            player.y -= climb_speed
            y_velocity = 0
            # opcionalmente manter jumps_left para permitir pulo após escalada
            # jumps_left = max_jumps

        #mover o inimigo
        mover()

        # Colisão com o inimigo
        if player.colliderect(enemy):
            morreu = True


        #colisao com o final
        if player.colliderect(final):
            passou = True

        #desenhando as parada da tela
        screen.fill(blue)
        
        # Desenhar plataformas 
        for platform in plataformas:
            pygame.draw.rect(screen, yellow, platform)
            
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
    clock.tick(65)


pygame.quit()