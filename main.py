# main.py
import pygame
from recursos.config import *
from recursos.sprites import *
from recursos.funcoes import *
from recursos.map_manager import MapManager

import sys

class Game:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((1000,700))
        self.clock = pygame.time.Clock()
        #self.font = pygame.font.Font('Arial',32)
        self.rodando = True

    def novo(self):
        self.jogando = True
        self.pausado = False
        
        self.todos_sprites = pygame.sprite.LayeredUpdates()
        self.obstaculos = pygame.sprite.LayeredUpdates()
        self.paredes = pygame.sprite.LayeredUpdates()
        self.meta = pygame.sprite.LayeredUpdates()

        self.map_manager = MapManager(self)
        self.player = Player(self, 450, 500)
        self.monitor = Monitor(self, 10, 0)


        self.map_manager.adicionar_nova_linha()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogando = False
                self.rodando = False
            if evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE:
                if self.pausado == True: self.pausado = False
                else:
                    self.pausado = True 
                    print_jogo = pygame.image.tobytes(self.tela,'RGBA')
                    str_jogo_pausado = pygame.image.frombytes(print_jogo,(1000,700),'RGBA')
                    self.img_jogo_pausado = pygame.transform.box_blur(str_jogo_pausado,INTENSIDADE_BLUR)
                    self.tela.blit(self.img_jogo_pausado,(0,0))
                    pygame.display.update()
                    self.img_jogo_pausado = pygame.transform.gaussian_blur(str_jogo_pausado,INTENSIDADE_BLUR)
                    self.tela.blit(self.img_jogo_pausado,(0,0))
                    pygame.display.update()
    def update(self):
        #Método update que vem do Layered Updates que defini antes,
        #ele vai percorrer todos sprites que estão no grupo e vai procurar o método update deles.
        self.map_manager.atualizar()
        self.todos_sprites.update()


    def draw(self):
        self.tela.fill(BLACK)
        self.todos_sprites.draw(self.tela)
        self.clock.tick(FPS)
        
        pygame.display.update()

    def main(self):
        # loop do jogo
        while self.jogando:
            self.eventos()
            if self.pausado == False:
                self.update()
                self.draw()
            else: pass
        self.rodando = False

    def game_over(self):
        pass

    def tela_inicial(self):
        pass

g = Game()
g.tela_inicial()
g.novo()

while g.rodando:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()