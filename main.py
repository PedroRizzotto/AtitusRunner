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
        pygame.display.set_caption('Atitus Survivor')
        self.tela = pygame.display.set_mode((LARGURA_TELA,ALTURA_TELA))
        self.clock = pygame.time.Clock()
        icone = pygame.image.load('recursos/icon.png')
        pygame.display.set_icon(icone)
        self.fonte_texto_vidas = pygame.font.Font('recursos/PressStart2P.ttf',15)
        self.fonte_como_pausar = pygame.font.Font('recursos/PressStart2P.ttf',8)
        self.fonte_menu = pygame.font.Font('recursos/PressStart2P.ttf',50)
        self.fonte_menu_menor = pygame.font.Font('recursos/PressStart2P.ttf',20)
        self.rodando = True

    def novo(self):
        self.pontuacao_atual = 0
        self.jogando = True
        self.pausado = False
        
        self.todos_sprites = pygame.sprite.LayeredUpdates()
        self.obstaculos = pygame.sprite.LayeredUpdates()
        self.paredes = pygame.sprite.LayeredUpdates()
        self.efeitos = pygame.sprite.LayeredUpdates()
        self.meta = pygame.sprite.LayeredUpdates()
        

        self.map_manager = MapManager(self)
        self.player = Player(self, 450, 500)
        self.monitor = Placar(self, 20, 1)

        self.map_manager.adicionar_nova_linha()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogando = False
                self.rodando = False
            if evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE:
                if self.pausado == True: self.pausado = False
                else: self.menu_pausa()

    def update(self):
        #Método update que vem do Layered Updates que defini antes,
        #ele vai percorrer todos sprites que estão no grupo e vai procurar o método update deles.
        self.map_manager.atualizar()
        self.todos_sprites.update()
        self.pontuacao_atual += 1

    def draw(self):
        self.tela.fill(BLACK)
        self.todos_sprites.draw(self.tela)
        self.player.debug_draw_hitbox(self.tela)
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
        self.jogando = False
        print('game over')

    def tela_inicial(self):
        pass

    def menu_pausa(self):
        self.pausado = True
        print_jogo = pygame.image.tobytes(self.tela,'RGBA')
        str_jogo_pausado = pygame.image.frombytes(print_jogo,(1000,700),'RGBA')
        self.img_jogo_pausado = pygame.transform.box_blur(str_jogo_pausado,INTENSIDADE_BLUR) # BLUR MAIS RÁPIDO PARA PAUSAR NA HORA
        self.tela.blit(self.img_jogo_pausado,(0,0))

        # texto grande pausado
        texto_pausado = self.fonte_menu.render("Jogo Pausado!",True,WHITE)
        texto_pausado_width, texto_pausado_height = self.fonte_menu.size("Jogo Pausado!")
        
        # texto menor em baixo dizendo como voltar ao jogo
        texto_como_voltar = self.fonte_menu_menor.render("Pressione <Esc> para voltar ao jogo",True,WHITE)
        texto_como_voltar_width, texto_como_voltar_height = self.fonte_menu_menor.size("Pressione <Esc> para voltar ao jogo")
    
        self.tela.blit(texto_pausado,((LARGURA_TELA / 2 - texto_pausado_width / 2),(ALTURA_TELA / 2 - texto_pausado_height)))
        self.tela.blit(texto_como_voltar,((LARGURA_TELA / 2 - texto_como_voltar_width / 2),(ALTURA_TELA / 2 - texto_como_voltar_height + texto_pausado_height )))
        pygame.display.update()
        self.img_jogo_pausado = pygame.transform.gaussian_blur(str_jogo_pausado,INTENSIDADE_BLUR) # BLUR MAIS LENTO MAS MAIS BONITO
        self.tela.blit(self.img_jogo_pausado,(0,0))
        
        # texto
        self.tela.blit(texto_pausado,((LARGURA_TELA / 2 - texto_pausado_width / 2),(ALTURA_TELA / 2 - texto_pausado_height)))
        self.tela.blit(texto_como_voltar,((LARGURA_TELA / 2 - texto_como_voltar_width / 2),(ALTURA_TELA / 2 - texto_como_voltar_height + texto_pausado_height )))

        pygame.display.update()
    

g = Game()
g.tela_inicial()
g.novo()

while g.rodando:
    g.main()
    g.game_over()

pygame.quit()
sys.exit()