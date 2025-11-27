import pygame
import os


class Player(pygame.Rect):
    def __init__(self, x, y, size, world_width):
        super().__init__(x, y, size, size)

        self.world_width = world_width

        # Na minha concepção esses números ficaram bons, mas se quiser brincar um pouco pode alterar eles.
        # Caso altere, e esqueceu quais números tava antes: 3, 1.82, -8, -22 respectivamente.
        self.speed = 3
        self.gravity = 1.82
        self.velocity_y = -8
        self.jump_force = -22

        self.direction = 1
        self.is_running = False
        self.on_ground = False  # <<< IMPORTANTÍSSIMO

        self.sprites_idle = []
        self.sprites_run = []
        self.current_frame = 0
        self.animation_speed = 0.2

        self.load_sprites()

    def load_sprites(self):
        base = os.path.join("game", "assets", "images")

        idle = os.path.join(base, "player_idle.png")
        self.sprites_idle = [pygame.image.load(idle).convert_alpha()]

        run = os.path.join(base, "player_run.png")
        sheet = pygame.image.load(run).convert_alpha()

        fw = sheet.get_width() // 7
        fh = sheet.get_height()

        self.sprites_run = [
            sheet.subsurface((i * fw, 0, fw, fh))
            for i in range(7)
        ]

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_force
            self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        self.is_running = False

        # Movimento horizontal
        if keys[pygame.K_a]:
            self.x -= self.speed
            self.direction = -1
            self.is_running = True

        if keys[pygame.K_d]:
            self.x += self.speed
            self.direction = 1
            self.is_running = True

        # Gravidade
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Colisão com plataformas
        self.check_platform_collision(platforms)

        # -----------------------------------------
        #  EVITAR QUE O PLAYER SAIA DA TELA
        # -----------------------------------------
        if self.x < 0:
            self.x = 0

        if self.right > self.world_width:
            self.right = self.world_width

    def check_platform_collision(self, platforms):
        self.on_ground = False

        for plat in platforms:
            # <<< SE plat é Plataforma, devemos usar plat.rect
            rect = plat.rect if hasattr(plat, "rect") else plat

            if self.colliderect(rect):

                if self.velocity_y > 0:
                    self.bottom = rect.top
                    self.velocity_y = 0
                    self.on_ground = True

                elif self.velocity_y < 0:
                    self.top = rect.bottom
                    self.velocity_y = 0

    def draw(self, screen):
        frames = self.sprites_run if self.is_running else self.sprites_idle

        self.current_frame += self.animation_speed
        if self.current_frame >= len(frames):
            self.current_frame = 0

        img = frames[int(self.current_frame)]

        if self.direction < 0:
            img = pygame.transform.flip(img, True, False)

        screen.blit(img, (self.x, self.y))

    def reset(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.current_frame = 0
        self.on_ground = False
