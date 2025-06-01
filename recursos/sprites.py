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

        self.image_raw = pygame.image.load("recursos/texturas/sprites/sprite_lobo_idle.png")

        self.image = pygame.transform.scale(self.image_raw,(self.largura,self.altura))
        #isso seria tipo a hitbox da imagem
    
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.movimento()

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