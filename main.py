###############################################
##             ATITUS SURVIVOR               ##
##                 06/2025                   ##
## Por: Pedro Henrique Rizzotto - RA: 138024 ##

import pygame
from recursos.funcoes import cls

cls()

pygame.init()
tamanhoJanela = (1000,700)
clock = pygame.time.Clock()
tela = pygame.display.set_mode(tamanhoJanela)
pygame.display.set_caption("Atitus Survivor")
icone = pygame.image.load("recursos/icon.png")
pygame.display.set_icon(icone)
branco = (255,255,255)

global rodando
rodando = True

def start():
    global rodando
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(branco)
        
        pygame.display.update()
        clock.tick(60)

start()