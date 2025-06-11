# main.py
import sys
import pygame # esse é o pygame-ce, versão atualizada e mantida pela comunidade.
            # Então Marcão se tu for testar rodar esse código -> pip uninstall pygame -> pip install pygame-ce
            # é totalmente backwards-compatible com os jogos em pygame normal, mas esse tem algumas funções novas que utilizei
from recursos.config import *
from recursos.telas import *
from recursos.sprites import *
from recursos.funcoes import *
from recursos.map_manager import MapManager

class Game:
    def __init__(self,tela):
        self.tela = tela
        self.clock = pygame.time.Clock()
        self.fonte_scoreboard = pygame.font.Font('recursos/PressStart2P.ttf',15)
        self.fonte_texto_vidas = pygame.font.Font('recursos/PressStart2P.ttf',15)
        self.fonte_como_pausar = pygame.font.Font('recursos/PressStart2P.ttf',8)
        self.fonte_menu = pygame.font.Font('recursos/PressStart2P.ttf',50)
        self.fonte_menu_menor = pygame.font.Font('recursos/PressStart2P.ttf',20)
        self.fonte_game_over = pygame.font.Font('recursos/PressStart2P.ttf',60)
        self.fonte_game_over_1 = pygame.font.Font('recursos/PressStart2P.ttf',80)
        self.fonte_scores_finais = pygame.font.Font('recursos/PressStart2P.ttf',17)
        self.caminhos_nanos = ["recursos/texturas/nanos/DevJunior.png"]
        self.rodando = True

    def novo(self,nome):
        self.nome = nome
        self.vidas = 3
        self.distancia_percorrida = 0
        self.pontuacao = 0
        self.conhecimento = 0
        self.conhecimento_scoreboard = 0
        self.networking = 0
        self.nanos_coletados = 0

        self.jogando = True
        self.pausado = False
        self.gerar_obstaculos = True
        self.gerar_conhecimento = True
        
        self.todos_sprites = pygame.sprite.LayeredUpdates()
        self.obstaculos = pygame.sprite.LayeredUpdates()
        self.itens = pygame.sprite.LayeredUpdates()
        self.paredes = pygame.sprite.LayeredUpdates()
        self.efeitos = pygame.sprite.LayeredUpdates()
        self.meta = pygame.sprite.LayeredUpdates()
        self.particulas = pygame.sprite.LayeredUpdates()

        self.map_manager = MapManager(self)
        self.player = Player(self, 450, 500)
        self.monitor = Monitor(self, 20, 1)
        self.scoreboard = Scoreboard(self,20)
        self.drone = Drone(self,200,400)

        self.map_manager.adicionar_nova_linha()

    def eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.jogando = False
                self.rodando = False
            if evento.type == pygame.KEYUP and evento.key == pygame.K_ESCAPE:
                if self.pausado == True: self.pausado = False
                else: self.menu_pausa()

            #eventos de debug
            if evento.type == pygame.KEYUP and evento.key == pygame.K_F13:
                self.vidas = 3
                self.gerar_obstaculos = True
                self.gerar_conhecimento = True
            if evento.type == pygame.KEYUP and evento.key == pygame.K_F14:
                self.vidas = 0
                self.gerar_obstaculos = False
                self.gerar_conhecimento = False
                
    def update(self):
        #Método update que vem do Layered Updates que defini antes,
        #ele vai percorrer todos sprites que estão no grupo e vai procurar o método update deles.
        self.map_manager.atualizar()
        self.todos_sprites.update()
        self.distancia_percorrida += 1

    def draw(self):
        self.tela.fill(BLACK)
        self.todos_sprites.draw(self.tela)
        #self.player.debug_draw_hitbox(self.tela)
        # for sprite in self.todos_sprites:
        #     if hasattr(sprite, 'debug_draw_hitbox'):
        #         sprite.debug_draw_hitbox(self.tela)
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


    
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Atitus Runner')
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    icone = pygame.image.load('recursos/icon.png')
    pygame.display.set_icon(icone)

    while True:
        # inicia a tela inicial
        nome = TelaInicial(tela).exibir()

        inicializar_banco_dados()
        g = Game(tela)
        g.novo(nome)

        # roda o jogo
        while g.rodando:
            g.main()

        TelaGameOver(tela).exibir()
        # depois de sair dessa tela, volta para a tela inicial.