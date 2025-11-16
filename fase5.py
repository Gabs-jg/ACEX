import pygame
from pygame.locals import *

pygame.init()

# Resolução da tela ajustada para 640x360
screen_width = 640
screen_height = 360
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Fase 5')

try:
    background_img_original = pygame.image.load('assets/background.jpg').convert()
    # Redimensionar para o novo tamanho da tela (640x360)
    background_img = pygame.transform.scale(background_img_original, (screen_width, screen_height))
except pygame.error as e:
    print(f"Não foi possível carregar a imagem de background. Verifique se o arquivo background.jpg está na pasta 'assets'. Erro: {e}")
    # Cria uma superfície preta caso a imagem não carregue
    background_img = pygame.Surface((screen_width, screen_height))
    background_img.fill((0, 0, 0))

# Criar um background mais largo para repetição
background_width = int(screen_width * 1.4)
try:
    # Redimensionar a imagem original para a largura maior
    background_extended = pygame.transform.scale(background_img_original, (background_width, screen_height))
except:
    # Fallback se não conseguir carregar a imagem
    background_extended = pygame.Surface((background_width, screen_height))
    background_extended.fill((0, 0, 0))

#cores
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
blue = (0,100,255)
red = (255,0,0)
magenta = (255,0,255)
yellow = (255, 255, 0) # Cor para as novas plataformas

#chão
ground_height = 30 # Reduzida a altura do chão
ground = pygame.Rect(0, screen_height - ground_height, background_width, ground_height)

# MESMO NÚMERO DE PLATAFORMAS DO EXEMPLO (3 plataformas)
plataformas = [
    pygame.Rect(80, screen_height - ground_height - 60, 100, 15),  # P1: y = 360-30-60 = 270
    pygame.Rect(260, screen_height - ground_height - 120, 120, 15), # P2: y = 360-30-120 = 210  
    pygame.Rect(450, screen_height - ground_height - 80, 100, 15)  # P3: y = 360-30-80 = 250
]

#final - PORTA PARA FINALIZAR O NÍVEL
final_syze = 30 # Tamanho ajustado
# Posiciona a porta logo após a última plataforma (450 + 100 = 550, então 560 fica logo depois)
final = pygame.Rect(560, ground.top - final_syze, final_syze, final_syze)

passou = False

#enemy - AGORA PATRULHA APENAS ENTRE O COMEÇO E A PORTA
enemy_syze = 25 # Tamanho um pouco menor
enemy = pygame.Rect(300, ground.top - enemy_syze, enemy_syze, enemy_syze)  # Começa no meio do percurso
morreu = False
enemy_speed = 3 # Velocidade ajustada
# O inimigo agora patrulha apenas entre o começo da fase e a porta
borda_esquerda = 100  # Um pouco depois do começo
borda_direita = final.left - 20  # Um pouco antes da porta

#personagem
player_size = 25 # Tamanho ajustado
player = pygame.Rect(0, 0, player_size,player_size)
player.bottomleft = (50, ground.top) # Começa um pouco à direita para a câmera

#gravidade e pulo
y_velocity = 0
gravity = 0.5
is_on_ground = False
jump = -8 # Força do pulo ajustada
# VARIÁVEIS PARA DOUBLE JUMP
max_jumps = 2  
jumps_left = max_jumps

# Variáveis para a nova mecânica de DASH
dash_speed = 40 # Velocidade do dash ajustada
is_dashing = False
dash_direction = 1 
can_dash = True 

# Variável para rastrear a direção do personagem para o dash
player_direction = 1 

# --- parâmetros de escalada ---
climb_speed = 4    
side_touch_buffer = 5  

# Variáveis da câmera
camera_x = 0
player_offset = screen_width // 3  # Jogador fica a 1/3 da tela à esquerda (estilo Mario)

#função para o inimigo de mover - AGORA PATRULHA APENAS ENTRE COMEÇO E PORTA
def mover():
    global enemy, enemy_speed, borda_direita, borda_esquerda
    enemy.x += enemy_speed

    # Inverte direção ao atingir as bordas entre começo e porta
    if enemy.left <= borda_esquerda or enemy.right >= borda_direita:
        enemy_speed *= -1

# Função para atualizar a câmera
def update_camera():
    global camera_x
    # A câmera segue o jogador, mantendo-o a 1/3 da tela à esquerda
    target_camera_x = player.x - player_offset
    
    # Limitar a câmera para não mostrar áreas fora do mundo
    camera_x = max(0, min(target_camera_x, background_width - screen_width))

# Função para aplicar o deslocamento da câmera a um retângulo
def apply_camera(rect):
    return rect.move(-camera_x, 0)

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

# Função para colisões horizontais
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
    # manter dentro do mundo
    player.left = max(0, player.left)
    player.right = min(background_width, player.right)

# Função para verificar colisão com plataformas (FIXADO CONTRA TUNNELING)
def check_platform_collision():
    global player, y_velocity, is_on_ground, jumps_left, can_dash 
    
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
                can_dash = True 
            # Bateu a cabeça embaixo da plataforma ao subir
            elif prev_bottom >= platform.bottom and player.top <= platform.bottom and y_velocity < 0:
                player.top = platform.bottom
                y_velocity = 0
            else:
                # Caso de colisão ambígua (p.ex. teletransporte), empurre para fora verticalmente
                if player.centery < platform.centery:
                    player.bottom = platform.top
                    y_velocity = 0
                    is_on_ground = True
                    on_platform = True
                    jumps_left = max_jumps
                    can_dash = True 
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
        can_dash = True 

    if not on_platform:
        is_on_ground = False

#função pra reiniciar o jogo
def reiniciar_jogo():
    global player, y_velocity, is_on_ground, passou, morreu, enemy, enemy_speed, player_direction, is_dashing, can_dash, jumps_left, camera_x
    # Reposiciona o player no canto inferior esquerdo
    player.bottomleft = (50, ground.top)

    # Reposiciona o inimigo no meio do percurso
    enemy.x = 300
    enemy.bottom = ground.top

    enemy_speed = 3
    y_velocity = 0
    is_on_ground = False

    passou = False
    morreu = False
    
    is_dashing = False 
    can_dash = True
    player_direction = 1
    jumps_left = max_jumps 
    camera_x = 0

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
                    is_on_ground = False 

                # DASH (Avanço) com a tecla 'E'
                if event.key == K_e and can_dash and not is_dashing:
                    is_dashing = True
                    can_dash = False 
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == K_r:
                    reiniciar_jogo()

    if not passou and not morreu:
        #movimento esquerda e direita
        keys = pygame.key.get_pressed()
        
        dx = 0
        if keys[K_a]:
            dx = -4 # Velocidade horizontal ajustada
            player_direction = -1 
        if keys[K_d]:
            dx = 4 # Velocidade horizontal ajustada
            player_direction = 1 
            
        # Lógica do DASH (Avanço)
        if is_dashing:
            dx = dash_speed * player_direction
            is_dashing = False 
            
        # Aplicar movimentação horizontal com checagem de colisão
        check_horizontal_collision(dx)

        # gravidade do personagem (aplicada a y_velocity)
        y_velocity += gravity

        # Aplicamos movimento vertical
        player.y += y_velocity

        # Verifica e corrige colisões verticais (pouso, cabeça)
        check_platform_collision()

        # MECÂNICA: ESCALAR QUANDO ESTÁ ENCOSTANDO LATERALMENTE
        lado = touching_platform_side()
        # se estiver encostando na lateral e pressionar W, sobe (e cancela a queda)
        if lado is not None and keys[K_w]:
            player.y -= climb_speed
            y_velocity = 0

        #mover o inimigo
        mover()

        # Atualizar a câmera
        update_camera()

        # Colisão com o inimigo
        if player.colliderect(enemy):
            morreu = True

        #colisao com o final
        if player.colliderect(final):
            passou = True

        #desenhando as parada da tela
        # DESENHO: Background com repetição
        screen.blit(background_extended, (0, 0), (camera_x, 0, screen_width, screen_height))
        
        # Desenhar plataformas (aplicando câmera)
        for platform in plataformas:
            platform_rect = apply_camera(platform)
            pygame.draw.rect(screen, yellow, platform_rect)
            
        # Desenhar outros elementos (aplicando câmera)
        pygame.draw.rect(screen, red, apply_camera(player))
        pygame.draw.rect(screen, green, apply_camera(ground))
        pygame.draw.rect(screen, black, apply_camera(final))
        pygame.draw.rect(screen, magenta, apply_camera(enemy))
        
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