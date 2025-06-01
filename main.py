# main.py
import pygame
from recursos.config import *
from recursos.sprites import *
from recursos.funcoes import *
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
        
        self.todos_sprites = pygame.sprite.LayeredUpdates()
        self.blocos = pygame.sprite.LayeredUpdates()
        self.inimigos = pygame.sprite.LayeredUpdates()

        self.player = Player(self, 1, 2)

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogando = False
                self.rodando = False
    def update(self):
        #Método update que vem do Layered Updates que defini antes,
        #ele vai percorrer todos sprites que estão no grupo e vai procurar o método update deles.
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
            self.update()
            self.draw()
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