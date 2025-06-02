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

    def update(self):
        self.movimento()
        self.animar()

        self.rect.x += self.movimentacao_x
        self.colisao()

        self.movimentacao_x = 0
        self.movendo = False

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
            if self.rect.colliderect(parede.rect):
                hits.append(parede)

        for parede in hits:
            if self.movimentacao_x > 0:
                self.rect.right = parede.rect.left
            elif self.movimentacao_x < 0:
                self.rect.left = parede.rect.right

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.rect, 2)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = OBSTACULO_LAYER
        self.groups = self.game.todos_sprites, self.game.obstaculos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image_raw = pygame.image.load("recursos/texturas/tiles/chao_molhado.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (game.tela.get_width() // 5, game.tela.get_width() // 5))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        self.rect.y += VELOCIDADE_SCROLL  # rolagem para baixo
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

        self.image_raw = pygame.image.load("recursos/texturas/sprites/monitor.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_raw,(self.largura,self.altura))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.contador_animacao = 0
        self.direcao_animacao = 'aumentando'

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

        escala = 1 + self.contador_animacao * 0.00115 
        nova_largura = int(self.largura * escala)
        nova_altura = int(self.altura * escala)
        self.image = pygame.transform.scale(self.image_raw, (nova_largura, nova_altura))

        # Atualiza o retângulo para corresponder ao novo tamanho
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.animar()