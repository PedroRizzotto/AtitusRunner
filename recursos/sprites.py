import pygame
from recursos.config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.todos_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.largura = 200
        self.altura = 200
        self.x = x
        self.y = y
        self.movimentacao_x = 0
        self.direcao = 'frente'
        self.movendo = False
        self.tempo_imunidade = 0

        self.spritesheet = pygame.image.load("recursos/texturas/sprites/lobo_spritesheet.png").convert_alpha()
        self.image_raw = pygame.image.load("recursos/texturas/sprites/sprite_lobo_idle.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (self.largura, self.altura))

        # Calcular área visível e cortar a imagem
        self.hitbox_visible = self.calcular_area_visivel(self.image)
        self.image = self.image.subsurface(
            pygame.Rect(
                self.hitbox_visible['left'],
                self.hitbox_visible['top'],
                self.hitbox_visible['width'],
                self.hitbox_visible['height']
            )
        ).copy()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.offset_hitbox_top = 0.75  # 75% da altura para baixo
        self.hitbox_altura = int(self.rect.height * 0.25)  # 25% da altura
        self.atualizar_hitbox()


        # Animação
        self.frame_width = 64
        self.frame_height = 64
        self.total_frames = 5
        self.current_frame = 0
        self.frames = []

        for i in range(self.total_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frame_scaled = pygame.transform.scale(frame, (self.largura, self.altura))

            hitbox = self.calcular_area_visivel(frame_scaled)
            frame_visible = frame_scaled.subsurface(
                pygame.Rect(
                    hitbox['left'],
                    hitbox['top'],
                    hitbox['width'],
                    hitbox['height']
                )
            ).copy()
            self.frames.append(frame_visible)

        self.velocidade_animacao = VELOCIDADE_ANIMACAO_PLAYER
        self.contador_animacao = 0
        self.direcao_animacao = 1

    def calcular_area_visivel(self, imagem):
        width, height = imagem.get_size()
        left, right = width, 0
        top, bottom = height, 0
        found_pixel = False

        for y in range(height):
            for x in range(width):
                pixel = imagem.get_at((x, y))
                if pixel[3] > 50:
                    found_pixel = True
                    left = min(left, x)
                    right = max(right, x)
                    top = min(top, y)
                    bottom = max(bottom, y)

        if not found_pixel:
            return {
                'left': width // 4,
                'top': height // 4,
                'width': width // 2,
                'height': height // 2
            }

        return {
            'left': left,
            'top': top,
            'width': right - left + 1,
            'height': bottom - top + 1
        }
    
    def atualizar_hitbox(self):
        altura = self.hitbox_altura
        topo = self.rect.y + int(self.rect.height * self.offset_hitbox_top)
        self.hitbox = pygame.Rect(self.rect.x, topo, self.rect.width, altura)


    def update(self):
        if self.tempo_imunidade > 0:
            self.tempo_imunidade -= 1
        
        print(self.tempo_imunidade)

        self.movimento()
        self.animar()

        self.rect.x += self.movimentacao_x
        self.colisao()

        self.movimentacao_x = 0
        self.movendo = False

        self.atualizar_hitbox()

    def movimento(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.movimentacao_x -= VELOCIDADE_PLAYER
            self.direcao = 'esquerda'
            self.movendo = True
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.movimentacao_x += VELOCIDADE_PLAYER
            self.direcao = 'direita'
            self.movendo = True

    def animar(self):
        self.contador_animacao += self.velocidade_animacao
        if self.contador_animacao >= 1:
            self.current_frame += self.direcao_animacao
            if self.current_frame >= self.total_frames - 1:
                self.current_frame = self.total_frames - 1
                self.direcao_animacao = -1
            elif self.current_frame <= 0:
                self.current_frame = 0
                self.direcao_animacao = 1

            self.image = self.frames[self.current_frame]
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

            self.contador_animacao = 0

    def colisao(self):
        hits = []
        for parede in self.game.paredes:
            if self.hitbox.colliderect(parede.rect):
                hits.append(parede)

        for parede in hits:
            if self.movimentacao_x > 0:
                self.rect.right = parede.rect.left
            elif self.movimentacao_x < 0:
                self.rect.left = parede.rect.right

        hits = []
        for obstaculo in self.game.obstaculos:
            if self.hitbox.colliderect(obstaculo.rect):
                
                if self.tempo_imunidade == 0:
                    if self.game.monitor.vidas > 1:
                        self.game.monitor.vidas -= 1
                        self.tempo_imunidade = 30
                    else:
                        self.game.game_over()

                obstaculo_colidido_x = obstaculo.rect[0]
                obstaculo_colidido_y = obstaculo.rect[1]
                obstaculo.kill()
                tile = Ground(self.game,obstaculo_colidido_x,obstaculo_colidido_y)
                efeito_explosao = ExplosaoFumaca(self.game,obstaculo_colidido_x,obstaculo_colidido_y)
                for obstaculo in self.game.obstaculos:
                    obstaculo_x = obstaculo.rect[0]
                    obstaculo_y = obstaculo.rect[1]
                    if abs(obstaculo_y - obstaculo_colidido_x) < 201 and (obstaculo_y - obstaculo_colidido_y) < 201:
                        obstaculo.kill()
                        tile = Ground(self.game,obstaculo_x,obstaculo_y)
                        efeito_explosao = ExplosaoFumaca(self.game,obstaculo_x,obstaculo_y)

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.rect, 1)  # sprite inteiro
        pygame.draw.rect(tela, (255, 0, 0), self.hitbox, 2)  # hitbox real

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = OBSTACULO_LAYER
        self.groups = self.game.todos_sprites, self.game.obstaculos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image_raw = pygame.image.load("recursos/texturas/tiles/chao_molhado.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (game.tela.get_width() // 5, game.tela.get_width() // 5))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Hitbox customizada
        margem = 0.5 #porcentagem pra reduzir a hitbox
        self.hitbox = pygame.Rect(
            self.rect.left + self.rect.width / margem / 2,
            self.rect.top + self.rect.height * margem /2,
            self.rect.width * (1 - margem),
            self.rect.height * (1- margem)
        )

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (255,0,0),self.hitbox, 2)

    def update(self):
        self.rect.y += VELOCIDADE_SCROLL  # rolagem para baixo
        self.hitbox.y += VELOCIDADE_SCROLL # mover a hitbox tbm
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = OBSTACULO_LAYER
        self.groups = self.game.todos_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image_raw = pygame.image.load("recursos/texturas/tiles/chao_normal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (game.tela.get_width() // 5, game.tela.get_width() // 5))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += VELOCIDADE_SCROLL
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class Parede(pygame.sprite.Sprite):
    def __init__(self, game, x, y, lado, tipo_parede):
        self.game = game
        self._layer = PAREDE_LAYER
        self.groups = self.game.todos_sprites, self.game.paredes
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.largura = 100
        self.altura = 200
        if lado == 0:
            self.spritesheet = pygame.image.load("recursos/texturas/tiles/paredes_esquerda_spritesheet.png")
        else: 
            self.spritesheet = pygame.image.load("recursos/texturas/tiles/paredes_direita_spritesheet.png")

        self.quantidade_paredes = 4
        self.largura_textura = 25
        self.altura_textura = 50
        
        # Extrai todos os frames do spritesheet para movimento
        self.frames = []
        for i in range(self.quantidade_paredes):
            frame = pygame.Surface((self.largura_textura, self.altura_textura), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.largura_textura, 0, self.largura_textura, self.altura_textura))
            # Escala o frame para o tamanho da parede
            frame_scaled = pygame.transform.scale(frame, (self.largura, self.altura))
            self.frames.append(frame_scaled)
            
        self.image = self.frames[tipo_parede]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += VELOCIDADE_SCROLL  # rolagem para baixo
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class Monitor(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = META_LAYER
        self.groups = self.game.todos_sprites, self.game.meta
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.largura = 200
        self.altura = 200
        self.x = x
        self.y = y

        self.image_monitor = pygame.image.load("recursos/texturas/sprites/monitor.png").convert_alpha()
        self.image_raw = pygame.transform.scale(self.image_monitor, (self.largura, self.altura))
        self.image = self.image_raw.copy()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.contador_animacao = 0
        self.direcao_animacao = 'aumentando'

        # Corações
        self.vidas = 3  # Vidas do personagem

        self.tamanho_coracao = (35,35)

        self.coracoes_animados = []
        spritesheet = pygame.image.load("recursos/texturas/sprites/coracao_animado_spritesheet.png").convert_alpha()
        for i in range(8):
            frame = spritesheet.subsurface((i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, (self.tamanho_coracao))
            self.coracoes_animados.append(frame)

        self.coracao_morto_raw = pygame.image.load("recursos/texturas/sprites/coracao_morto.png").convert_alpha()
        self.coracao_morto = pygame.transform.scale(self.coracao_morto_raw, (self.tamanho_coracao))

        self.frame_atual = 0
        self.timer_animacao = 0
        self.intervalo_animacao = 100  # ms entre quadros

        self.texto_vidas = self.game.fonte_texto_vidas.render('Vidas',True,WHITE)
        self.texto_vidas_width, self.texto_vidas_height = self.game.fonte_texto_vidas.size('Vidas')

        self.texto_pausar = self.game.fonte_como_pausar.render('Press <Esc> to pause',True,WHITE)
        self.texto_pausar_width, self.texto_pausar_height = self.game.fonte_como_pausar.size('Press <Esc> to pause')


    def animar(self):
        if self.direcao_animacao == 'aumentando':
            if self.contador_animacao < 100:
                self.contador_animacao += 1
            else:
                self.direcao_animacao = 'diminuindo'
        else:
            if self.contador_animacao > 0:
                self.contador_animacao -= 1
            else:
                self.direcao_animacao = 'aumentando'

        self.escala = 1 + self.contador_animacao * 0.00115

    def atualizar_animacao_coracoes(self):
        agora = pygame.time.get_ticks()
        if agora - self.timer_animacao > self.intervalo_animacao:
            self.frame_atual = (self.frame_atual + 1) % len(self.coracoes_animados)
            self.timer_animacao = agora

    def desenhar_Monitor(self):
        # superfície base limpa com o tamanho do monitor
        self.superficie = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.superficie.blit(self.image_raw, (0, 0))  # Fundo do Monitor

        centro_x = self.largura // 2
        centro_y = self.altura // 2

        total_largura = 3 * self.tamanho_coracao[0] + 2 * 10
        inicio_x = centro_x - total_largura // 2

        for i in range(3):
            x = inicio_x + i * (self.tamanho_coracao[0] + 10)
            y = centro_y - 20 - self.tamanho_coracao[1] // 2
            if i < self.vidas:
                frame = self.coracoes_animados[self.frame_atual]
                self.superficie.blit(frame, (x, y))
            else:
                self.superficie.blit(self.coracao_morto, (x, y))

        self.superficie.blit(self.texto_vidas, (centro_x - self.texto_vidas_width // 2, centro_y - 60))
        self.superficie.blit(self.texto_pausar, (centro_x - self.texto_pausar_width // 2, centro_y + 10))

        # redimensiona toda a superfície final a partir da escala atual
        nova_largura = int(self.largura * self.escala)
        nova_altura = int(self.altura * self.escala)
        
        #pega a superfície e coloca como self.image pro pygame entender que é a img
        self.image = pygame.transform.smoothscale(self.superficie, (nova_largura, nova_altura)) 

    def update(self):
        self.animar()
        self.atualizar_animacao_coracoes()
        self.desenhar_Monitor()

        #atualiza a posicao do Monitor
        self.rect = self.image.get_rect(center=(self.x + self.largura // 2, self.y + self.altura // 2))

class ExplosaoFumaca(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.todos_sprites, self.game.efeitos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.largura = 256
        self.altura = 384
        self.x = x + 100
        self.y = y + 100

        self.spritesheet = pygame.image.load("recursos/texturas/sprites/explosao_fumaca_spritesheet_transparente.png").convert_alpha()

        # tamanho de cada sprite e o número de spritess
        self.total_frames = 7
        self.frame_width = 256
        self.frame_height = 384

        # loop pra extrair todos os quadros da spritesheet
        self.frames = []
        for i in range(self.total_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frame_scaled = pygame.transform.scale(frame, (self.largura, self.altura))
            self.frames.append(frame_scaled)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Controle de animação
        self.velocidade_animacao = VELOCIDADE_ANIMACAO_EXPLOSAO_FUMACA
        self.contador_animacao = 0

    def animar(self):
        self.contador_animacao += self.velocidade_animacao
        if self.contador_animacao >= 1:
            self.current_frame += 1
            self.contador_animacao = 0

            if self.current_frame >= self.total_frames:
                self.kill()
            else:
                self.image = self.frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

    def update(self):
        self.animar()
        self.rect.y += VELOCIDADE_SCROLL
        if self.rect.top > self.game.tela.get_height():
            self.kill()
