import pygame
import sys
import math
from recursos.config import *

class TelaInicial:
    def __init__(self, tela):
        self.tela = tela
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font('recursos/PressStart2P.ttf', 20)
        self.nome_inserido = ''
        self.entry_ativa = False
        self.estado = 'entry'  # 'entry' ou 'welcome'

        # Blur de fundo
        self.fundo = pygame.image.load("recursos/texturas/fachada_atitus.png")
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA_TELA, ALTURA_TELA))
        self.fundo = pygame.transform.gaussian_blur(self.fundo, 7)

        # Título do jogo
        self.titulo_jogo = pygame.image.load("recursos/texturas/titulo_jogo.png").convert_alpha()
        self.anim_amplitude = 7  # pixels
        self.anim_speed = 0.9    # oscilações por segundo

        # EntryBox
        self.entry_rect = pygame.Rect(200, 400, 600, 70)
        self.botao_entry = pygame.Rect(350, 490, 300, 70)

        # Botão começar
        self.botao_start = pygame.Rect(350, 530, 300, 70)

    def desenhar_retangulo_arredondado(self, surface, rect, cor_fundo, cor_borda, radius=20, largura_borda=4):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(s, cor_fundo, s.get_rect(), border_radius=radius)
        surface.blit(s, (rect.x, rect.y))
        pygame.draw.rect(surface, cor_borda, rect, width=largura_borda, border_radius=radius)

    def desenhar_entry(self):
        # Fundo e título
        self.tela.blit(self.fundo, (0, 0))
        t = pygame.time.get_ticks() / 1000.0
        offset_y = math.sin(2 * math.pi * self.anim_speed * t) * self.anim_amplitude
        x = (LARGURA_TELA - self.titulo_jogo.get_width()) // 2
        y = 50 + offset_y
        self.tela.blit(self.titulo_jogo, (x, y))

        # EntryBox
        cor_borda = pygame.Color('#195DA6')
        if self.entry_ativa:
            cor_borda = pygame.Color(75, 155, 255)
        self.desenhar_retangulo_arredondado(self.tela, self.entry_rect, (0,0,0,153), cor_borda)
        texto = self.nome_inserido or 'Digite seu nome...'
        txt = self.fonte.render(texto, True, (255,255,255))
        self.tela.blit(txt, (self.entry_rect.x+20,
                              self.entry_rect.y + (self.entry_rect.height-txt.get_height())//2))

        # Botão Confirmar
        mouse = pygame.mouse.get_pos()
        border = pygame.Color('#195DA6')
        if self.botao_entry.collidepoint(mouse): border = pygame.Color(75,155,255)
        self.desenhar_retangulo_arredondado(self.tela, self.botao_entry, (0,0,0,153), border)
        label = self.fonte.render('CONFIRMAR', True, (255,255,255))
        self.tela.blit(label, label.get_rect(center=self.botao_entry.center))

    def desenhar_welcome(self):
        # Fundo sem blur extra
        self.tela.fill((0,0,0))
        self.tela.blit(self.fundo, (0, 0))

        # Saudação
        prefixo = "Olá"
        palavra_riscada = "mundo"
        sufixo = f", {self.nome_inserido}!"

        # Renderizar partes separadamente
        texto_prefixo = self.fonte.render(prefixo + " ", True, (255, 255, 255))
        texto_mundo = self.fonte.render(palavra_riscada, True, (255, 255, 255))
        texto_sufixo = self.fonte.render(sufixo, True, (255, 255, 255))

        # Calcular posição centralizada
        total_largura = texto_prefixo.get_width() + texto_mundo.get_width() + texto_sufixo.get_width()
        x_inicial = LARGURA_TELA // 2 - total_largura // 2
        y_texto = 200

        # Blit na tela
        self.tela.blit(texto_prefixo, (x_inicial, y_texto))
        self.tela.blit(texto_mundo, (x_inicial + texto_prefixo.get_width(), y_texto))
        self.tela.blit(texto_sufixo, (x_inicial + texto_prefixo.get_width() + texto_mundo.get_width(), y_texto))

        # Desenhar linha sobre "mundo"
        x_mundo = x_inicial + texto_prefixo.get_width()
        y_mundo = y_texto + texto_mundo.get_height() // 2
        pygame.draw.line(self.tela, (255, 255, 255), (x_mundo, y_mundo), (x_mundo + texto_mundo.get_width(), y_mundo), 2)

        # Explicação rápida
        linhas = [
            "Neste jogo você controla o personagem",
            "utilizando A e D ou as setas do teclado",
            "e deve desviar de obstáculos, coletar",
            "nano degrees, livros de conhecimento e",
            "networking para sobreviver até o fim."
        ]
        y0 = 280
        for l in linhas:
            txt = self.fonte.render(l, True, (200,200,200))
            self.tela.blit(txt, (LARGURA_TELA//2 - txt.get_width()//2, y0))
            y0 += txt.get_height() + 5

        # Botão Iniciar
        mouse = pygame.mouse.get_pos()
        border = pygame.Color('#195DA6')
        if self.botao_start.collidepoint(mouse): border = pygame.Color(75,155,255)
        self.desenhar_retangulo_arredondado(self.tela, self.botao_start, (0,0,0,153), border)
        label = self.fonte.render('JOGAR', True, (255,255,255))
        self.tela.blit(label, label.get_rect(center=self.botao_start.center))

    def processar_eventos(self, evt):
        if evt.type == pygame.MOUSEBUTTONDOWN:
            if self.estado == 'entry':
                if self.entry_rect.collidepoint(evt.pos): self.entry_ativa = True
                else: self.entry_ativa = False
                if self.botao_entry.collidepoint(evt.pos) and self.nome_inserido.strip():
                    self.estado = 'welcome'
            elif self.estado == 'welcome':
                if self.botao_start.collidepoint(evt.pos):
                    return True
        if self.estado == 'entry' and evt.type == pygame.KEYDOWN and self.entry_ativa:
            if evt.key == pygame.K_BACKSPACE:
                self.nome_inserido = self.nome_inserido[:-1]
            elif len(self.nome_inserido) < 14 and evt.unicode.isprintable():
                self.nome_inserido += evt.unicode
        return False

    def exibir(self):
        while True:
            for evt in pygame.event.get():
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.processar_eventos(evt):
                    return self.nome_inserido
            if self.estado == 'entry':
                self.desenhar_entry()
            else:
                self.desenhar_welcome()
            pygame.display.update()
            self.relogio.tick(FPS)