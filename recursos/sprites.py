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

        self.x = x * 64
        self.y = y * 64
        self.largura = 200
        self.altura = 200

        self.image_raw = pygame.image.load("recursos/texturas/sprites/sprite_lobo_idle.png")

        self.image = pygame.transform.scale(self.image_raw,(self.largura,self.altura))
        #isso seria tipo a hitbox da imagem
    
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        pass

