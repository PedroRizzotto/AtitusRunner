import pygame
from recursos.config import *
from recursos.funcoes import *
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
        self.tempo_imunidade = 0

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

        self.offset_hitbox_top = 0.75  # 75% da altura para baixo
        self.hitbox_altura = int(self.rect.height * 0.25)  # 25% da altura
        self.offset_hitbox_x = 0.40
        self.hitbox_largura = int(self.rect.width * 0.60) # hitbox dos pés
        self.atualizar_hitbox()


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
    
    def atualizar_hitbox(self):
        altura = self.hitbox_altura
        largura = self.hitbox_largura
        topo = self.rect.y + int(self.rect.height * self.offset_hitbox_top)
        lado = self.rect.x + int(self.rect.width * self.offset_hitbox_x // 2)
        self.hitbox = pygame.Rect(lado, topo, largura, altura)


    def update(self):
        if self.tempo_imunidade > 0:
            self.tempo_imunidade -= 1

        self.movimento()
        self.animar()
        self.atualizar_hitbox()
        self.gerar_mask_hitbox()

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

    def gerar_mask_hitbox(self):
        mask_surface = pygame.Surface((self.hitbox.width, self.hitbox.height), pygame.SRCALPHA)
        # Copia da imagem somente a parte da hitbox
        src_x = self.hitbox.left - self.rect.left
        src_y = self.hitbox.top - self.rect.top
        mask_surface.blit(self.image, (0, 0), pygame.Rect(src_x, src_y, self.hitbox.width, self.hitbox.height))
        self.hitbox_mask = pygame.mask.from_surface(mask_surface)

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

        hits = []
        for obstaculo in self.game.obstaculos:
            offset_x = obstaculo.rect.left - self.hitbox.left
            offset_y = obstaculo.rect.top - self.hitbox.top
            if self.hitbox_mask.overlap(obstaculo.mask, (offset_x, offset_y)):
                
                if self.tempo_imunidade == 0:
                    if self.game.vidas > 1:
                        self.game.vidas -= 1
                        self.tempo_imunidade = 30
                    else:
                        escrever_dados(self.game.nome, self.game.nanos_coletados, 
                                    self.game.pontuacao, self.game.conhecimento, self.game.networking)
                        self.game.jogando = False

                obstaculo_colidido_x = obstaculo.rect[0]
                obstaculo_colidido_y = obstaculo.rect[1]
                obstaculo.kill()
                efeito_explosao = ExplosaoFumaca(self.game, obstaculo_colidido_x, obstaculo_colidido_y)
                for obstaculo in self.game.obstaculos:
                    obstaculo_x = obstaculo.rect[0]
                    obstaculo_y = obstaculo.rect[1]
                    if abs(obstaculo_y - obstaculo_colidido_x) < 201 and (obstaculo_y - obstaculo_colidido_y) < 201:
                        obstaculo.kill()
                        efeito_explosao = ExplosaoFumaca(self.game, obstaculo_x, obstaculo_y)
        
        hits = []
        for item in self.game.itens:
            offset_x = item.rect.left - self.hitbox.left
            offset_y = item.rect.top - self.hitbox.top
            if self.hitbox_mask.overlap(item.mask, (offset_x, offset_y)):     
                
                self.game.conhecimento += 1

                # MUDANÇA PRINCIPAL: Em vez de destruir imediatamente, inicia animação
                if isinstance(item, Conhecimento):
                    item.iniciar_coleta()
                else:
                    # Para outros tipos de item, manter comportamento original
                    item_colidido_x = item.rect[0]
                    item_colidido_y = item.rect[1]
                    item.kill()
                    efeito_explosao = ExplosaoFumaca(self.game, item_colidido_x, item_colidido_y)

    def coletou_powerup(self):
        for _ in range(60):  # ou 40 para mais impacto
            ParticulaExplosaoNeon(self.game, self)

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (0, 255, 0), self.rect, 1)  # sprite inteiro
        pygame.draw.rect(tela, (255, 0, 0), self.hitbox, 2)  # hitbox real

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, game, x, y,caminho_imagem, largura, altura):
        self.game = game
        self._layer = OBSTACULO_LAYER
        self.groups = self.game.todos_sprites, self.game.obstaculos
        pygame.sprite.Sprite.__init__(self, self.groups)

        largura = largura
        altura = altura 

        self.image_raw = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (largura, altura))
        self.rect = self.image.get_rect(center=(x, y))

        self.mask = pygame.mask.from_surface(self.image)

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (255,0,0),self.rect, 2)

    def update(self):
        self.rect.y += VELOCIDADE_SCROLL  # rolagem para baixo
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class PocaAgua(Obstacle):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "recursos/texturas/tiles/chao_molhado.png", 135, 135)

class CarrinhoTI(Obstacle):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "recursos/texturas/tiles/carrinho_ti_idle.png", 200, 200)

class Item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, caminho_imagem, largura, altura):
        self.game = game
        self._layer = PAREDE_LAYER
        self.groups = self.game.todos_sprites, self.game.itens
        pygame.sprite.Sprite.__init__(self, self.groups)

        largura = largura
        altura = altura 

        self.image_raw = pygame.image.load(caminho_imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (largura, altura))
        self.rect = self.image.get_rect(center=(x, y))

        self.mask = pygame.mask.from_surface(self.image)

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (255,0,0), self.rect, 2)

    def update(self):
        self.rect.y += VELOCIDADE_SCROLL  # rolagem para baixo
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class Conhecimento(Item):
    def __init__(self, game, x, y):
        super().__init__(game, x, y, "recursos/texturas/itens/livro_conhecimento.png", 80, 80)
        
        # Estados da animação
        self.coletado = False
        self.tempo_animacao = 0
        self.duracao_animacao = 60  # frames para completar a animação
        
        # Posições para a animação (serão definidas quando coletado)
        self.pos_inicial_x = 0
        self.pos_inicial_y = 0
        self.pos_final_x = 900
        self.pos_final_y = 40
        
        # Tamanhos para a animação
        self.tamanho_inicial = 75
        self.tamanho_final = 20
        
        # Controle de curva
        self.altura_curva = -200  # Altura da curva (negativo para curva para cima)
    
    def iniciar_coleta(self):

        # Captura a posição ATUAL do item quando coletado
        self.pos_inicial_x = self.rect.centerx
        self.pos_inicial_y = self.rect.centery
        
        self.coletado = True
        self.tempo_animacao = 0
        
        # Muda o layer para ficar acima dos outros elementos
        self._layer = 999  # Layer bem alto para ficar na frente
        
        # Remove APENAS do grupo de itens para não ser coletado novamente
        # Mantém em todos_sprites para continuar chamando update()
        if self in self.game.itens:
            self.game.itens.remove(self)
        
    def update(self):
        if not self.coletado:
            # Comportamento normal - rolar para baixo
            super().update()
        else:
            # Animação de coleta
            self.tempo_animacao += 1
            
            # Progresso da animação (0 a 1)
            progresso = self.tempo_animacao / self.duracao_animacao
            
            if progresso >= 1.0:
                # Animação completa - destruir o item
                self.game.conhecimento_scoreboard += 1
                self.kill()
                return
            
            # Função de easing para suavizar a animação
            # Usando easing quadrático para acelerar no final
            t = progresso * progresso
            
            # Calcular posição na curva exponencial/bezier
            # Ponto de controle da curva no meio do caminho
            meio_x = (self.pos_inicial_x + self.pos_final_x) / 2
            meio_y = (self.pos_inicial_y + self.pos_final_y) / 2 + self.altura_curva
            
            # Curva quadrática de Bézier
            # P(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
            inv_t = 1 - t
            
            new_x = (inv_t * inv_t * self.pos_inicial_x + 
                    2 * inv_t * t * meio_x + 
                    t * t * self.pos_final_x)
            
            new_y = (inv_t * inv_t * self.pos_inicial_y + 
                    2 * inv_t * t * meio_y + 
                    t * t * self.pos_final_y)
            
            # Interpolar tamanho
            novo_tamanho = int(self.tamanho_inicial + 
                             (self.tamanho_final - self.tamanho_inicial) * t)
            
            # Garantir que o tamanho não seja menor que 1
            novo_tamanho = max(1, novo_tamanho)
            
            # Atualizar imagem com novo tamanho
            self.image = pygame.transform.scale(self.image_raw, (novo_tamanho, novo_tamanho))
            
            # Atualizar posição
            self.rect = self.image.get_rect(center=(int(new_x), int(new_y)))
            
            # Atualizar máscara para o novo tamanho
            self.mask = pygame.mask.from_surface(self.image)

class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y,obstaculo):
        self.game = game
        self._layer = OBSTACULO_LAYER
        self.groups = self.game.todos_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image_raw = pygame.image.load("recursos/texturas/tiles/chao_normal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image_raw, (game.tela.get_width() // 5, game.tela.get_width() // 5))
        self.rect = self.image.get_rect(topleft=(x, y))

        if obstaculo == '1':
            sorteio_obs = random.randint(1,2)
            if sorteio_obs == 1:
                obstaculo = PocaAgua(self.game,self.rect.centerx,self.rect.centery)
            elif sorteio_obs == 2:
                obstaculo = CarrinhoTI(self.game,self.rect.centerx,self.rect.centery)

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

    def debug_draw_hitbox(self, tela):
        pygame.draw.rect(tela, (255,0,0),self.rect, 2)

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

        self.image_monitor = pygame.image.load("recursos/texturas/sprites/monitor.png").convert_alpha()
        self.image_raw = pygame.transform.scale(self.image_monitor, (self.largura, self.altura))
        self.image = self.image_raw.copy()

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.contador_animacao = 0
        self.direcao_animacao = 'aumentando'

        self.tamanho_coracao = (35,35)

        self.coracoes_animados = []
        spritesheet = pygame.image.load("recursos/texturas/sprites/coracao_animado_spritesheet.png").convert_alpha()
        for i in range(8):
            frame = spritesheet.subsurface((i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, (self.tamanho_coracao))
            self.coracoes_animados.append(frame)

        self.coracao_morto_raw = pygame.image.load("recursos/texturas/sprites/coracao_morto.png").convert_alpha()
        self.coracao_morto = pygame.transform.scale(self.coracao_morto_raw, (self.tamanho_coracao))

        self.frame_atual = 0
        self.timer_animacao = 0
        self.intervalo_animacao = 100  # ms entre quadros

        self.texto_vidas = self.game.fonte_texto_vidas.render('Vidas',True,WHITE)
        self.texto_vidas_width, self.texto_vidas_height = self.game.fonte_texto_vidas.size('Vidas')

        self.texto_pausar = self.game.fonte_como_pausar.render('Press <Esc> to pause',True,WHITE)
        self.texto_pausar_width, self.texto_pausar_height = self.game.fonte_como_pausar.size('Press <Esc> to pause')


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

        self.escala = 1 + self.contador_animacao * 0.00115

    def atualizar_animacao_coracoes(self):
        agora = pygame.time.get_ticks()
        if agora - self.timer_animacao > self.intervalo_animacao:
            self.frame_atual = (self.frame_atual + 1) % len(self.coracoes_animados)
            self.timer_animacao = agora

    def desenhar_Monitor(self):
        # superfície base limpa com o tamanho do monitor
        self.superficie = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.superficie.blit(self.image_raw, (0, 0))  # Fundo do Monitor

        centro_x = self.largura // 2
        centro_y = self.altura // 2

        total_largura = 3 * self.tamanho_coracao[0] + 2 * 10
        inicio_x = centro_x - total_largura // 2

        for i in range(3):
            x = inicio_x + i * (self.tamanho_coracao[0] + 10)
            y = centro_y - 20 - self.tamanho_coracao[1] // 2
            if i < self.game.vidas:
                frame = self.coracoes_animados[self.frame_atual]
                self.superficie.blit(frame, (x, y))
            else:
                self.superficie.blit(self.coracao_morto, (x, y))

        self.superficie.blit(self.texto_vidas, (centro_x - self.texto_vidas_width // 2, centro_y - 60))
        self.superficie.blit(self.texto_pausar, (centro_x - self.texto_pausar_width // 2, centro_y + 10))

        # redimensiona toda a superfície final a partir da escala atual
        nova_largura = int(self.largura * self.escala)
        nova_altura = int(self.altura * self.escala)
        
        #pega a superfície e coloca como self.image pro pygame entender que é a img
        self.image = pygame.transform.smoothscale(self.superficie, (nova_largura, nova_altura)) 

    def update(self):
        self.animar()
        self.atualizar_animacao_coracoes()
        self.desenhar_Monitor()

        #atualiza a posicao do Monitor
        self.rect = self.image.get_rect(center=(self.x + self.largura // 2, self.y + self.altura // 2))

class Scoreboard(pygame.sprite.Sprite):
    def __init__(self, game, y):
        self.game = game
        self._layer = META_LAYER
        self.groups = self.game.todos_sprites, self.game.meta
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game.conhecimento_scoreboard = self.game.conhecimento

        self.largura = 270
        self.altura = 75

        self.x = LARGURA_TELA - self.largura - 10
        self.y = y

        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # Atualiza o valor de pontuacao baseado na distância percorrida
        self.game.pontuacao = self.game.distancia_percorrida // 20

        # Atualiza a imagem do placar
        self.image.fill((0, 0, 0, 0))  # Limpa com transparência

        # Desenha o fundo preto com 80% de transparência (opacidade 51 em 255)
        pygame.draw.rect(
            self.image,
            (0, 0, 0, 204),  # Preto com alfa 204 (~80%)
            pygame.Rect(0, 0, self.largura, self.altura),
            border_radius=7
        )

        # Renderiza os textos
        fonte = self.game.fonte_scoreboard
        texto_pontuacao = fonte.render(f"Pontuação: {self.game.pontuacao}", True, (255, 255, 255))
        texto_conhecimento = fonte.render(f"Conhecimento: {self.game.conhecimento_scoreboard}", True, (255, 255, 255))
        texto_networking = fonte.render(f"Networking: {self.game.networking}", True, (255, 255, 255))

        # Blita os textos na tela
        self.image.blit(texto_pontuacao, (10, 5))
        self.image.blit(texto_conhecimento, (10, 30))
        self.image.blit(texto_networking, (10, 55))



class ExplosaoFumaca(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.todos_sprites, self.game.efeitos
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.largura = 256
        self.altura = 384
        self.x = x + 100
        self.y = y + 100

        self.spritesheet = pygame.image.load("recursos/texturas/sprites/explosao_fumaca_spritesheet_transparente.png").convert_alpha()

        # tamanho de cada sprite e o número de spritess
        self.total_frames = 7
        self.frame_width = 256
        self.frame_height = 384

        # loop pra extrair todos os quadros da spritesheet
        self.frames = []
        for i in range(self.total_frames):
            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.spritesheet, (0, 0), (i * self.frame_width, 0, self.frame_width, self.frame_height))
            frame_scaled = pygame.transform.scale(frame, (self.largura, self.altura))
            self.frames.append(frame_scaled)

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # Controle de animação
        self.velocidade_animacao = VELOCIDADE_ANIMACAO_EXPLOSAO_FUMACA
        self.contador_animacao = 0

    def animar(self):
        self.contador_animacao += self.velocidade_animacao
        if self.contador_animacao >= 1:
            self.current_frame += 1
            self.contador_animacao = 0

            if self.current_frame >= self.total_frames:
                self.kill()
            else:
                self.image = self.frames[self.current_frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center

    def update(self):
        self.animar()
        self.rect.y += VELOCIDADE_SCROLL
        if self.rect.top > self.game.tela.get_height():
            self.kill()

class ParticulaExplosaoNeon(pygame.sprite.Sprite):
    def __init__(self, game, player):
        self.game = game
        self._layer = PLAYER_LAYER + 1
        self.groups = game.todos_sprites, game.particulas
        pygame.sprite.Sprite.__init__(self, self.groups)

        # Cores neon vibrantes
        cores_neon = [
            (57, 255, 20),   # verde limão neon
            (0, 255, 255),   # ciano
            (255, 20, 147),  # rosa choque
            (0, 191, 255),   # azul neon
            (255, 255, 0),   # amarelo vivo
            (255, 0, 255),   # magenta
        ]
        self.cor = random.choice(cores_neon)

        # Tamanho do retângulo (retângulo vertical tipo barra de energia)
        self.largura = 2
        self.altura = 8
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.cor, (0, 0, self.largura, self.altura), border_radius=1)
        self.rect = self.image.get_rect()

        # Distribuição ao redor do player - altura total, largura parcial
        player_center = player.rect.center
        player_width = player.rect.width
        player_height = player.rect.height

        offset_x = random.randint(-player_width // 2, player_width // 2)
        offset_y = random.randint(-player_height // 2, player_height // 2)
        self.pos = pygame.math.Vector2(player_center[0] + offset_x, player_center[1] + offset_y)
        self.rect.center = self.pos

        # Movimento: suave para cima, pode ter leve desvio lateral
        self.vel = pygame.math.Vector2(random.uniform(-0.3, 0.3), random.uniform(-1.2, -0.4))
        self.alpha = 255
        self.fade_speed = random.randint(5, 9)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos

        # Fade out
        self.alpha -= self.fade_speed
        if self.alpha <= 0:
            self.kill()
        else:
            self.image.set_alpha(self.alpha)