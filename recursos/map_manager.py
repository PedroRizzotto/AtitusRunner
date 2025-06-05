# recursos/map_manager.py

import random
import pygame
from recursos.sprites import Obstacle, Ground, Parede
from recursos.config import *

class MapManager:
    def __init__(self, game):
        self.game = game
        self.largura_linha = 4  # número de colunas por linha
        self.tamanho_tile = 800 // self.largura_linha
        self.altura_tela = game.tela.get_height()
        self.linhas_ativas = []

        #criar as primeiras linhas vazias:
        y_pos = 0
        for linha in range(0,4):
            parede_esquerda = Parede(self.game, 0, y_pos,0,random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
            parede_direita = Parede(self.game, 900, y_pos,1,random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
            for coluna in range(0,self.largura_linha):
                x = 100 + (coluna * self.tamanho_tile)
                tile = Ground(self.game, x, y_pos)
            y_pos += 200

    def gerar_linha_aleatoria(self):
        dificuldade = 0.2
        linha = ""
        for _ in range(self.largura_linha):
            linha += "1" if random.random() < dificuldade else "0"

        if linha.count("1") == self.largura_linha:
            index = random.randint(0, self.largura_linha - 1)
            linha = linha[:index] + "0" + linha[index + 1:]

        return linha

    def adicionar_nova_linha(self):

        nova_linha_str = self.gerar_linha_aleatoria()
        y_pos = -self.tamanho_tile
        nova_linha = []  # ← lista de sprites da linha

        for i, char in enumerate(nova_linha_str):
            x = 100 + (i * self.tamanho_tile)
            if char == "1":
                tile = Obstacle(self.game, x, y_pos)
            else:
                tile = Ground(self.game, x, y_pos)
            nova_linha.append(tile)

        parede_esquerda = Parede(self.game, 0, y_pos,0,random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
        parede_direita = Parede(self.game, 900, y_pos,1,random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
        nova_linha.append(parede_esquerda)
        nova_linha.append(parede_direita)

        self.linhas_ativas.append(nova_linha)


    def atualizar(self):
        # Remove linhas onde todos os tiles já foram mortos
        self.linhas_ativas = [linha for linha in self.linhas_ativas if any(tile.alive() for tile in linha)]

        # Verifica se é necessário adicionar nova linha no topo
        if not self.linhas_ativas:
            self.adicionar_nova_linha()
        else:
            linha_mais_alta = self.linhas_ativas[-1]
            tile_topo = min(tile.rect.y for tile in linha_mais_alta)

            if tile_topo >= 0:  # Está na tela, então ainda há espaço acima
                self.adicionar_nova_linha()

