# recursos/map_manager.py

import random
import pygame
from recursos.sprites import Obstacle, Ground, Parede, Conhecimento
from recursos.config import *

class MapManager:
    def __init__(self, game):
        self.game = game
        self.largura_linha = 4  # número de colunas por linha
        self.tamanho_tile = 800 // self.largura_linha
        self.altura_tela = game.tela.get_height()
        self.linhas_ativas = []
        
        # Configurações para geração de conhecimentos
        self.conhecimento_patterns = {
            'single': 0.3,      # Conhecimento único
            'line': 0.4,        # Linha de conhecimentos
            'zigzag': 0.2,      # Padrão zigzag
            'arc': 0.1          # Padrão em arco
        }
        self.conhecimento_spawn_chance = 0.6  # 60% de chance de spawnar conhecimentos em uma linha
        self.consecutive_conhecimento_lines = 0  # Contador para evitar muitas linhas seguidas com conhecimentos

        # Criar as primeiras linhas vazias:
        y_pos = 0
        for linha in range(0, 4):
            parede_esquerda = Parede(self.game, 0, y_pos, 0, random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
            parede_direita = Parede(self.game, 900, y_pos, 1, random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
            for coluna in range(0, self.largura_linha):
                x = 100 + (coluna * self.tamanho_tile)
                tile = Ground(self.game, x, y_pos, '0')
            y_pos += 200

    def gerar_linha_livre(self):
        linha = "0000"
        return linha

    def gerar_linha_aleatoria(self):
        dificuldade = 0.2
        linha = ""
        for _ in range(self.largura_linha):
            linha += "1" if random.random() < dificuldade else "0"

        if linha.count("1") == self.largura_linha:
            index = random.randint(0, self.largura_linha - 1)
            linha = linha[:index] + "0" + linha[index + 1:]

        return linha

    def get_available_positions(self, linha_str):
        available = []
        for i, char in enumerate(linha_str):
            if char == '0':  # Posição livre (sem obstáculo)
                available.append(i)
        return available

    def generate_conhecimento_pattern(self, available_positions, y_pos):
        if not available_positions:
            return []
        
        conhecimentos = []
        pattern = random.choices(list(self.conhecimento_patterns.keys()), 
                               weights=list(self.conhecimento_patterns.values()))[0]
        
        if pattern == 'single':
            # Conhecimento único em posição aleatória
            pos = random.choice(available_positions)
            x = 100 + (pos * self.tamanho_tile) + self.tamanho_tile // 2
            conhecimentos.append(Conhecimento(self.game, x, y_pos + 50))
            
        elif pattern == 'line':
            # Linha de conhecimentos consecutivos
            if len(available_positions) >= 2:
                # Escolhe quantos conhecimentos consecutivos (2-4)
                num_conhecimentos = min(random.randint(2, 4), len(available_positions))
                
                # Encontra sequências consecutivas de posições disponíveis
                consecutive_groups = self.find_consecutive_groups(available_positions)
                
                if consecutive_groups:
                    # Escolhe um grupo que tenha pelo menos num_conhecimentos posições
                    valid_groups = [group for group in consecutive_groups if len(group) >= num_conhecimentos]
                    if valid_groups:
                        chosen_group = random.choice(valid_groups)
                        start_idx = random.randint(0, len(chosen_group) - num_conhecimentos)
                        
                        for i in range(num_conhecimentos):
                            pos = chosen_group[start_idx + i]
                            x = 100 + (pos * self.tamanho_tile) + self.tamanho_tile // 2
                            conhecimentos.append(Conhecimento(self.game, x, y_pos + 50))
            
        elif pattern == 'zigzag':
            # Padrão zigzag (alternado)
            if len(available_positions) >= 2:
                selected_positions = available_positions[::2]  # Pega posições alternadas
                for pos in selected_positions[:3]:  # Máximo 3 conhecimentos no zigzag
                    x = 100 + (pos * self.tamanho_tile) + self.tamanho_tile // 2
                    conhecimentos.append(Conhecimento(self.game, x, y_pos + 50))
                    
        elif pattern == 'arc':
            # Padrão em arco (conhecimentos nas extremidades)
            if len(available_positions) >= 2:
                # Pega primeira e última posição disponível
                positions = [available_positions[0], available_positions[-1]]
                # Se há posições no meio, pode adicionar uma
                if len(available_positions) >= 3:
                    middle_idx = len(available_positions) // 2
                    positions.append(available_positions[middle_idx])
                
                for pos in positions:
                    x = 100 + (pos * self.tamanho_tile) + self.tamanho_tile // 2
                    conhecimentos.append(Conhecimento(self.game, x, y_pos + 50))
        
        return conhecimentos

    def find_consecutive_groups(self, positions):
        # Encontra grupos de posições consecutivas
        if not positions:
            return []
        
        groups = []
        current_group = [positions[0]]
        
        for i in range(1, len(positions)):
            if positions[i] == positions[i-1] + 1:
                current_group.append(positions[i])
            else:
                if len(current_group) > 1:
                    groups.append(current_group)
                current_group = [positions[i]]
        
        if len(current_group) > 1:
            groups.append(current_group)
        
        return groups

    def should_spawn_conhecimento(self):
        # Reduz chance se já teve muitas linhas consecutivas com conhecimentos
        if not self.game.gerar_conhecimento:
            chance = 0
        elif self.consecutive_conhecimento_lines >= 3:
            chance = self.conhecimento_spawn_chance * 0.3
        elif self.consecutive_conhecimento_lines >= 2:
            chance = self.conhecimento_spawn_chance * 0.6
        else:
            chance = self.conhecimento_spawn_chance
        
        should_spawn = random.random() < chance
        return should_spawn

    def adicionar_nova_linha(self):
        
        if self.game.gerar_obstaculos: nova_linha_str = self.gerar_linha_aleatoria()
        else: nova_linha_str = self.gerar_linha_livre()
        
        y_pos = -self.tamanho_tile
        nova_linha = []  # ← lista de sprites da linha

        # Criar tiles da linha
        for i, char in enumerate(nova_linha_str):
            x = 100 + (i * self.tamanho_tile)
            tile = Ground(self.game, x, y_pos, char)
            nova_linha.append(tile)

        # Criar paredes
        parede_esquerda = Parede(self.game, 0, y_pos, 0, random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
        parede_direita = Parede(self.game, 900, y_pos, 1, random.choices(TIPOS_PAREDE, weights=PROBABILIDADE_PAREDE, k=1)[0])
        nova_linha.append(parede_esquerda)
        nova_linha.append(parede_direita)

        # Gerar conhecimentos se necessário
        try:
            if self.should_spawn_conhecimento():
                available_positions = self.get_available_positions(nova_linha_str)
                
                conhecimentos = self.generate_conhecimento_pattern(available_positions, y_pos)
                
                # Adicionar conhecimentos à linha
                nova_linha.extend(conhecimentos)
                self.consecutive_conhecimento_lines += 1
            else:
                self.consecutive_conhecimento_lines = 0
        except Exception as e:
            pass # ignora o erro kk (ou seja, n gera nenhum conhecimento)

        self.linhas_ativas.append(nova_linha)

    def atualizar(self):        
        # Remove linhas onde todos os tiles já foram mortos
        linhas_antes = len(self.linhas_ativas)
        self.linhas_ativas = [linha for linha in self.linhas_ativas if any(tile.alive() for tile in linha)]
        linhas_removidas = linhas_antes - len(self.linhas_ativas)

        # Verifica se é necessário adicionar nova linha no topo
        if not self.linhas_ativas:
            self.adicionar_nova_linha()
        else:
            linha_mais_alta = self.linhas_ativas[-1]
            tile_topo = min(tile.rect.y for tile in linha_mais_alta if hasattr(tile, 'rect'))

            if tile_topo >= 0:  # Está na tela, então ainda há espaço acima
                self.adicionar_nova_linha()

    def get_all_conhecimentos(self):
        # retorna todos os conhecimentos ativos no mapa
        conhecimentos = []
        for linha in self.linhas_ativas:
            for sprite in linha:
                if isinstance(sprite, Conhecimento):
                    conhecimentos.append(sprite)
        return conhecimentos