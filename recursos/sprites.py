#sprites.py

import pygame
from recursos.config import *
import math
import random

class Player(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.todos_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.largura = 200
        self.altura = 200
        self.x = 400
        self.y = 500

        self.movimentacao_x = 0

        # utilizado para saber em que direção o personagem está indo para as animações WIP
        self.direcao = 'frente'
        self.movendo = True


        #spreadsheet com a animação
        self.spritesheet = pygame.image.load("recursos/texturas/sprites/lobo_spritesheet.png").convert_alpha()

        # Player parado
        self.image_raw = pygame.image.load("recursos/texturas/sprites/sprite_lobo_idle.png")
        self.image = pygame.transform.scale(self.image_raw,(self.largura,self.altura))
       
        #isso seria tipo a hitbox da imagem
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # Configurações da animação
        self.frame_width = 64
        self.frame_height = 64
        self.total_frames = 5
        self.current_frame = 0

        # Extrai todos os frames do spritesheet para movimento
        self.frames = []
        for i in range(self.total_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            # Escala o frame para o tamanho do player
            frame_scaled = pygame.transform.scale(frame, (self.largura, self.altura))
            self.frames.append(frame_scaled)

        self.image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        

        self.velocidade_animacao = 0.20  # Velocidade da animação
        self.contador_animacao = 0
        self.direcao_animacao = 1 

    def update(self):
        self.movimento()

        if self.movendo:
            self.animar()
        else:
            self.image = self.image
            self.current_frame = 0
            self.contador_animacao = 0
            self.direcao_animacao = 1

        self.rect.x += self.movimentacao_x
        self.movimentacao_x = 0


    def movimento(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
           self.movimentacao_x -= VELOCIDADE_PLAYER
           self.direcao = 'esquerda'
        elif teclas [pygame.K_RIGHT]:
            self.movimentacao_x += VELOCIDADE_PLAYER
            self.direcao = 'direita'
        elif teclas[pygame.K_a]:
           self.movimentacao_x -= VELOCIDADE_PLAYER
           self.direcao = 'esquerda'
        elif teclas [pygame.K_d]:
            self.movimentacao_x += VELOCIDADE_PLAYER
            self.direcao = 'direita'

    def animar(self):
        self.contador_animacao += self.velocidade_animacao
        if self.contador_animacao >= 1:
            self.current_frame += self.direcao_animacao

            if self.current_frame >= self.total_frames -1:
                self.current_frame = self.total_frames -1
                self.direcao_animacao = -1
            elif self.current_frame <= 0:
                self.current_frame = 0
                self.direcao_animacao = 1

            #atualiza a img

            self.image = self.frames[self.current_frame]
            self.contador_animacao = 0



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
        self.rect.y += 2  # rolagem para baixo
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
        self.rect.y += 2
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class Parede(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PAREDE_LAYER
        self.groups = self.game.todos_sprites
        pygame.sprite.Sprite.__init__(self,self.groups)

        self.largura = 200
        self.altura = 200