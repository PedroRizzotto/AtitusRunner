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

    def game_over(self):
        def desenhar_historico(screen, fonte_scores_finais, x=50, y=350):
            
            # Dimensões do retângulo
            largura = 600
            altura = 250
            
            # Criar surface para o retângulo com transparência
            historico_surface = pygame.Surface((largura, altura))
            historico_surface.set_alpha(255 * 0.2)  # 80% de transparencia
            historico_surface.fill(BLACK)
            
            # Desenhar o retângulo na tela
            screen.blit(historico_surface, (x, y))
            
            # Obter os últimos registros
            registros = obter_ultimos_registros(5)
            
            # Configurações de texto
            cor_texto = (255, 255, 255)  # Branco
            espacamento_linha = 30
            
            # Desenhar cabeçalho
            cabecalho = "Nome/Data/Hora    Nanos    Pontuação    Conhecimento    Networking"
            texto_cabecalho = fonte_scores_finais.render(cabecalho, True, cor_texto)
            screen.blit(texto_cabecalho, (x + 10, y + 10))
            
            # Desenhar linha separadora
            pygame.draw.line(screen, cor_texto, 
                            (x + 10, y + 40), 
                            (x + largura - 10, y + 40), 2)
            
            # Desenhar os registros
            for i, (chave, dados) in enumerate(registros):
                # Limitar o tamanho da chave para caber na tela
                chave_display = chave[:20] + "..." if len(chave) > 20 else chave
                
                # Verificar se dados é tupla/lista ou dicionário
                if isinstance(dados, (list, tuple)):
                    # Formato: (nanos, pontuacao, conhecimento, networking, data, hora)
                    nanos = dados[0] if len(dados) > 0 else 0
                    pontuacao = dados[1] if len(dados) > 1 else 0
                    conhecimento = dados[2] if len(dados) > 2 else 0
                    networking = dados[3] if len(dados) > 3 else 0
                elif isinstance(dados, dict):
                    # Formato dicionário (seu caso)
                    nanos = dados.get('nanos', 0)
                    pontuacao = dados.get('pontuacao', 0)
                    conhecimento = dados.get('conhecimento', 0)
                    networking = dados.get('networking', 0)
                else:
                    # Fallback
                    nanos = pontuacao = conhecimento = networking = 0
                
                # Formatar linha com nome e hora (extrair do final da chave)
                # A chave tem formato: "nome dd/mm/yyyy hh:mm:ss"
                partes_chave = chave.split(' ')
                if len(partes_chave) >= 3:
                    nome = partes_chave[0]
                    hora_display = partes_chave[-1]  # última parte é a hora
                    nome_hora = f"{nome} {hora_display}"
                else:
                    nome_hora = chave[:20]
                
                # Truncar se muito longo
                nome_hora = nome_hora[:25] + "..." if len(nome_hora) > 25 else nome_hora
                
                linha = f"{nome_hora:<28} {nanos:<8} {pontuacao:<11} {conhecimento:<13} {networking}"
                
                # Renderizar e desenhar texto
                texto_linha = fonte_scores_finais.render(linha, True, cor_texto)
                screen.blit(texto_linha, (x + 10, y + 55 + (i * espacamento_linha)))
            
            # Se não houver registros suficientes, preencher com linhas vazias
            for i in range(len(registros), 5):
                linha_vazia = "-" * 60
                texto_vazio = fonte_scores_finais.render(linha_vazia, True, (128, 128, 128))  # Cinza
                screen.blit(texto_vazio, (x + 10, y + 55 + (i * espacamento_linha)))

        #self.pausado = True
        print_jogo = pygame.image.tobytes(self.tela,'RGBA')
        str_jogo_pausado = pygame.image.frombytes(print_jogo,(1000,700),'RGBA')
        self.img_jogo_pausado = pygame.transform.box_blur(str_jogo_pausado,INTENSIDADE_BLUR) # BLUR MAIS RÁPIDO PARA PAUSAR NA HORA
        self.tela.blit(self.img_jogo_pausado,(0,0))

        # texto grande pausado
        texto_game_over = self.fonte_game_over_1.render("GAME OVER",True,RED)
        texto_game_over_width, texto_game_over_height = self.fonte_game_over_1.size("GAME OVER")

        self.tela.blit(texto_game_over,((LARGURA_TELA / 2 - texto_game_over_width / 2),(ALTURA_TELA / 2 - texto_game_over_height - 200)))
        pygame.display.update()

        print_jogo = pygame.image.tobytes(self.tela,'RGBA')
        str_jogo_pausado = pygame.image.frombytes(print_jogo,(1000,700),'RGBA')

        self.img_jogo_pausado = pygame.transform.gaussian_blur(str_jogo_pausado,INTENSIDADE_BLUR_GO) # BLUR MAIS LENTO MAS MAIS BONITO
        self.tela.blit(self.img_jogo_pausado,(0,0))
        
        # texto
        self.tela.blit(texto_game_over,((LARGURA_TELA / 2 - texto_game_over_width / 2),(ALTURA_TELA / 2 - texto_game_over_height-200)))

        desenhar_historico(self.tela,self.fonte_scores_finais)

        pygame.display.update()

        for i in range(0,1000000):
            print(i)

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


    tela_inicial = TelaInicial(tela)
    nome = tela_inicial.exibir()

    inicializar_banco_dados()
    g = Game(tela)
    g.novo(nome)

    while g.rodando:
        g.main()
        g.game_over()

    pygame.quit()
    sys.exit()