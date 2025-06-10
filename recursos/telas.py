import pygame
import sys
import math
import pyttsx3
from recursos.config import *

class TelaInicial:
    def __init__(self, tela):
        self.tela = tela
        self.relogio = pygame.time.Clock()
        self.fonte = pygame.font.Font('recursos/PressStart2P.ttf', 20)
        self.fonte_criado_por = pygame.font.Font('recursos/PressStart2P.ttf', 12)
        self.nome_inserido = ''
        self.entry_ativa = False
        self.estado = 'entry'  # 'entry' ou 'welcome'
        self.falou_nome = False

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
        txt = self.fonte.render(texto, True, WHITE)
        self.tela.blit(txt, (self.entry_rect.x+20,
                              self.entry_rect.y + (self.entry_rect.height-txt.get_height())//2))

        # Botão Confirmar
        mouse = pygame.mouse.get_pos()
        border = pygame.Color('#195DA6')
        if self.botao_entry.collidepoint(mouse): border = pygame.Color(75,155,255)
        self.desenhar_retangulo_arredondado(self.tela, self.botao_entry, (0,0,0,153), border)
        label = self.fonte.render('CONFIRMAR', True, WHITE)
        self.tela.blit(label, label.get_rect(center=self.botao_entry.center))

    def falar_nome(self):
        engine = pyttsx3.init()
        texto = f"Olá, {self.nome_inserido}"
        engine.say(texto)

        engine.runAndWait()

        self.falou_nome = True

    def desenhar_welcome(self):
        # Fundo sem blur extra
        self.tela.fill((0,0,0))
        self.tela.blit(self.fundo, (0, 0))

        # Saudação
        prefixo = "Olá"
        palavra_riscada = "mundo"
        sufixo = f", {self.nome_inserido}!"

        # Renderizar partes separadamente
        texto_prefixo = self.fonte.render(prefixo + " ", True, WHITE)
        texto_mundo = self.fonte.render(palavra_riscada, True, WHITE)
        texto_sufixo = self.fonte.render(sufixo, True, WHITE)

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
            elif len(self.nome_inserido) < 10 and evt.unicode.isprintable():
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
            if not self.falou_nome and self.estado == 'welcome': self.falar_nome()
            self.relogio.tick(FPS)


class TelaGameOver:
    def __init__(self, tela):
        import pygame
        from recursos.funcoes import obter_ultimos_registros
        self.tela = tela
        self.relogio = pygame.time.Clock()
        self.fonte_coluna = pygame.font.Font('recursos/PressStart2P.ttf', 17)
        self.fonte_celula = pygame.font.Font('recursos/PressStart2P.ttf', 20)
        self.fonte_botao = pygame.font.Font('recursos/PressStart2P.ttf', 30)
        self.records = obter_ultimos_registros(5)

        print_jogo = pygame.image.tobytes(tela,'RGBA')
        self.str_jogo_pausado = pygame.image.frombytes(print_jogo,(1000,700),'RGBA')
        self.img_jogo_pausado = pygame.transform.gaussian_blur(self.str_jogo_pausado,10) # BLUR MAIS LENTO MAS MAIS BONITO

        self.img_titulo_game_over = pygame.image.load("recursos/texturas/titulo_game_over.png").convert_alpha()
        
        # Botão de voltar/menu
        self.botao_rect = pygame.Rect(
            (LARGURA_TELA - 200) // 2, ALTURA_TELA - 120,
            200, 50
        )

    def desenhar(self):
        import pygame
        # Blur e fundo escuro
        self.tela.blit(self.img_jogo_pausado,(0,0))
        self.tela.blit(self.img_titulo_game_over,(0,0))

        # Cabeçalhos da tabela
        headers = ['Nome', 'Nanos', 'Pontuação', 'Conhecimento', 'Networking']
        col_widths = [200, 140, 200, 200, 200]
        x_start = (LARGURA_TELA - sum(col_widths)) // 2
        y_start = 300
        # desenha cabeçalho
        for i, text in enumerate(headers):
            hdr_surf = self.fonte_coluna.render(text, True, (255, 255, 255))
            x = x_start + sum(col_widths[:i]) + (col_widths[i] - hdr_surf.get_width()) // 2
            self.tela.blit(hdr_surf, (x, y_start))

        # linhas de dados
        line_h = 30
        for idx, (_, valores) in enumerate(self.records):
            y = y_start + 40 + idx * line_h
            # fundo alternado
            if idx % 2 == 0:
                row_bg = pygame.Surface((sum(col_widths), line_h))
                row_bg.set_alpha(100)
                row_bg.fill((50, 50, 50))
                self.tela.blit(row_bg, (x_start, y))
            # desenha cada coluna
            cols = [
                valores.get('nome',''),
                str(valores.get('nanos',0)),
                str(valores.get('pontuacao',0)),
                str(valores.get('conhecimento',0)),
                str(valores.get('networking',0))
            ]
            for j, col in enumerate(cols):
                cell_surf = self.fonte_celula.render(col, True, (255, 255, 255))
                x = x_start + sum(col_widths[:j]) + 50
                self.tela.blit(cell_surf, (x, y))

        # Botão Voltar
        
        btn_surf = pygame.Surface(self.botao_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            btn_surf,
            (0, 0, 0, 153),
            btn_surf.get_rect(),
            border_radius=20
        )
        self.tela.blit(btn_surf, self.botao_rect.topleft)
        # borda "neon"
        border_color = pygame.Color('#195DA6')
        if self.botao_rect.collidepoint(pygame.mouse.get_pos()):
            border_color = pygame.Color(75, 155, 255)
        pygame.draw.rect(
            self.tela,
            border_color,
            self.botao_rect,
            width=4,
            border_radius=20
        )
        # label
        label = self.fonte_botao.render('VOLTAR', True, (255, 255, 255))
        self.tela.blit(label, label.get_rect(center=self.botao_rect.center))

        pygame.display.update()

    def eventos(self, evento):
        import pygame
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if self.botao_rect.collidepoint(evento.pos):
                return True
        return False

    def exibir(self):
        import pygame
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if self.eventos(e):
                    return
            self.desenhar()
            self.relogio.tick(FPS)