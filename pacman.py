import pygame
import random
from abc import ABCMeta, abstractmethod


# Constantes
# Dimensões
LARGURA = 800
ALTURA = 600
DIMENSAO = (LARGURA, ALTURA)
RAIO = 30

# Movimento
VELOCIDADE = 1

# Tuplas de cores
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
BRANCO = (255, 255, 255)
CIANO = (0, 255, 255)
LARANJA = (255, 140, 0)
ROSA = (255, 15, 192)

# Direções
ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4

# Inicia o módulo
pygame.init()

# Surfaces
tela = pygame.display.set_mode(DIMENSAO, 0)
fonte = pygame.font.SysFont("arial", 20, True, False)

class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass

class Movimentavel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass

class Cenario(ElementoJogo):
    def __init__(self, tamanho, pacman):
        self.tamanho = tamanho
        self.pacman = pacman
        self.movimentaveis = []
        self.pontuacao = 0
        self.estado = "jogando"
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]
    
    def adicionar_movimentavel(self, objeto):
        self.movimentaveis.append(objeto)
    
    def pintar_pontuacao(self, tela):
        posicao_x = self.tamanho * 30

        imagem_pontuacao = fonte.render(f'Score: {self.pontuacao}', True, AMARELO)
        imagem_vidas = fonte.render(f'Vidas: {self.vidas}', True, AMARELO)

        tela.blit(imagem_pontuacao, (posicao_x, 50))
        tela.blit(imagem_vidas, (posicao_x, 100))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            posicao_x = numero_coluna * self.tamanho
            posicao_y = numero_linha * self.tamanho

            cor = PRETO   
            if coluna == 2:
                cor = AZUL

            pygame.draw.rect(tela, cor, (posicao_x, posicao_y, self.tamanho, self.tamanho), 0)

            if coluna == 1:
                posicao_x += (self.tamanho // 2)
                posicao_y += (self.tamanho // 2)

                pygame.draw.circle(tela, BRANCO, (posicao_x, posicao_y), self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == "jogando":
            self.pintar_jogando(tela)
        elif self.estado == "pausado":
            self.pintar_jogando(tela)
            self.pintar_texto_centro(tela, "P A U S A D O")
        elif self.estado == "gameover":
            self.pintar_jogando(tela)
            self.pintar_texto_centro(tela, "G A M E O V E R")
        elif self.estado == "vitoria":
            self.pintar_jogando(tela)
            self.pintar_texto_centro(tela, "V O C E  V E N C E U !")

    def pintar_texto_centro(self, tela, texto):
        imagem_texto = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - imagem_texto.get_width()) // 2
        texto_y = (tela.get_height() - imagem_texto.get_height()) // 2
        tela.blit(imagem_texto, (texto_x, texto_y))

    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_pontuacao(tela)

    def direcoes(self, linha, coluna):
        direcoes = []

        if self.matriz[int(linha) - 1][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha) + 1][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna) + 1] != 2:
            direcoes.append(DIREITA)

        return direcoes

    def calcular_regras(self):
        if self.estado == "jogando":
            self.calcular_regras_jogando()
        elif self.estado == "pausado":
            self.calcular_regras_pausado()
        elif self.estado == "gameover":
            self.calcular_regras_gameover

    def calcular_regras_gameover():
        ...

    def calcular_regras_pausado(self):
        pass

    def calcular_regras_jogando(self):
        for movimentavel in self.movimentaveis:
            linha = int(movimentavel.linha)
            coluna = int(movimentavel.coluna)
            linha_intencao = int(movimentavel.linha_intencao)
            coluna_intencao = int(movimentavel.coluna_intencao)

            direcoes = self.direcoes(linha, coluna)

            if len(direcoes) >= 3:
                movimentavel.esquina(direcoes)

            if isinstance(movimentavel, Fantasma) and movimentavel.linha == self.pacman.linha and movimentavel.coluna == self.pacman.coluna:
                self.vidas -= 1

                if self.vidas <= 0:
                    self.estado = "gameover"
                else:
                    self.pacman.linha = 1
                    self.pacman.coluna = 1
            else:
                if 0 <= coluna_intencao < 28 and 0 <= linha_intencao < 29 and self.matriz[linha_intencao][coluna_intencao] != 2:
                    movimentavel.aceitar_movimento()
                    if isinstance(movimentavel, Pacman) and self.matriz[linha][coluna] == 1:
                        self.pontuacao += 1
                        self.matriz[linha][coluna] = 0
                        if self.pontuacao >= 306:
                            self.estado = "vitoria"
                else:
                    movimentavel.recusar_movimento(direcoes)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.QUIT:
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_p:
                    if self.estado == "jogando":
                        self.estado = "pausado"
                    else:
                        self.estado = "jogando"

class Pacman(ElementoJogo, Movimentavel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.posicao_x = 400
        self.posicao_y = 300
        self.tamanho = tamanho
        # 800 // 30 # tamanho proporcinal a uma area de 800 pixels divididos em 30 células, cada uma tendo aproximadamente 26 pixels
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.raio = self.tamanho // 2 # retorna a parte inteira da divisão
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.velocidade_abertura = 1
    
    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.velocidade_x
        self.linha_intencao = self.linha + self.velocidade_y
        self.posicao_x = int(self.coluna * self.tamanho + self.raio) # Pacman deixa de se movimentar por coordenadas de pixels e passa a se movimentar por um estratégia de coordenadas de linhas por colunas. Essa estratégia ganha sinergia com o uso de um cenário gerado por uma matriz de coordenadas.
        self.posicao_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        # Desenha o corpo
        pygame.draw.circle(tela, AMARELO, (self.posicao_x, self.posicao_y), self.raio, 0)

        self.abertura += self.velocidade_abertura

        if self.abertura > self.raio:
            self.velocidade_abertura = -1
        elif self.abertura <= 0:
            self.velocidade_abertura = 1

        # Desenha a boca
        canto_boca = (self.posicao_x, self.posicao_y)
        labio_superior = (self.posicao_x + self.raio, self.posicao_y - self.abertura)
        labio_inferior = (self.posicao_x + self.raio , self.posicao_y + self.abertura)
        boca = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, boca, 0)

        # Desenha o olho
        olho_x = int(self.posicao_x + self.raio / 3)
        olho_y = int(self.posicao_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)

        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    self.velocidade_x = VELOCIDADE
                elif evento.key == pygame.K_LEFT:
                    self.velocidade_x = -VELOCIDADE
                elif evento.key == pygame.K_UP:
                    self.velocidade_y = -VELOCIDADE
                elif evento.key == pygame.K_DOWN:
                    self.velocidade_y = VELOCIDADE
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                    self.velocidade_x = 0
                elif  evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    self.velocidade_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass

class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.velocidade = VELOCIDADE
        self.direcao = ABAIXO
        self.tamanho = tamanho
        self.cor = cor

    def pintar(self, tela):
        fatia = self.tamanho // 8
        posicao_x = int(self.coluna * self.tamanho)
        posicao_y = int(self.linha * self.tamanho)
        corpo = [(posicao_x, posicao_y + self.tamanho), 
            (posicao_x + fatia, posicao_y + fatia * 2),
            (posicao_x + fatia * 2, posicao_y + fatia // 2),
            (posicao_x + fatia * 3, posicao_y),
            (posicao_x + fatia * 5, posicao_y),
            (posicao_x + fatia * 6, posicao_y + fatia // 2),
            (posicao_x + fatia * 7, posicao_y + fatia * 2),
            (posicao_x + self.tamanho, posicao_y + self.tamanho)
        ]

        pygame.draw.polygon(tela, self.cor, corpo, 0)

        raio_olho_externo = fatia
        raio_olho_interno = fatia // 2

        olho_esq_x = int(posicao_x + fatia * 2.5)
        olho_esq_y = int(posicao_y + fatia * 2.5)
        olho_esquerdo = (olho_esq_x, olho_esq_y)

        olho_dir_x = int(posicao_x + fatia * 5.5)
        olho_dir_y = int(posicao_y + fatia * 2.5)
        olho_direito = (olho_dir_x, olho_dir_y)

        pygame.draw.circle(tela, BRANCO, olho_esquerdo, raio_olho_externo, 0)
        pygame.draw.circle(tela, PRETO, olho_esquerdo, raio_olho_interno, 0)

        pygame.draw.circle(tela, BRANCO, olho_direito, raio_olho_externo, 0)
        pygame.draw.circle(tela, PRETO, olho_direito, raio_olho_interno, 0)

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade    

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.coluna = self.coluna_intencao
        self.linha = self.linha_intencao

    def recusar_movimento(self, direcoes):
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha_intencao
        self.mudar_direcao(direcoes)

    def processar_eventos(self, eventos):
        pass

# Somente executado se o arquivo rodado for o atual, não chamado se a execução vier de um import.
if __name__ == "__main__":
    pacman = Pacman(600 // 30)
    fantasma_blinky = Fantasma(VERMELHO, 600 // 30)
    fantasma_inky = Fantasma(CIANO, 600 // 30)
    fantasma_clyde = Fantasma(LARANJA, 600 // 30)
    fantasma_pinky = Fantasma(ROSA, 600 // 30)
    cenario = Cenario(600 // 30, pacman)

    cenario.adicionar_movimentavel(pacman)
    cenario.adicionar_movimentavel(fantasma_blinky)
    cenario.adicionar_movimentavel(fantasma_inky)
    cenario.adicionar_movimentavel(fantasma_clyde)
    cenario.adicionar_movimentavel(fantasma_pinky)

    # Loop do jogo
    while True:
        # calcula as regras
        pacman.calcular_regras()

        fantasma_blinky.calcular_regras()
        fantasma_inky.calcular_regras()
        fantasma_clyde.calcular_regras()
        fantasma_pinky.calcular_regras()

        cenario.calcular_regras()

        # Renderiza

        # Preenche a tela de preto a cada loop, para que as formas desenhadas sejam desenhadas na nova posição, sem que fique o rastro das posições antigas (bleeding)
        tela.fill(PRETO)
        
        cenario.pintar(tela)
        pacman.pintar(tela)
        fantasma_blinky.pintar(tela)
        fantasma_inky.pintar(tela)
        fantasma_clyde.pintar(tela)
        fantasma_pinky.pintar(tela)

        pygame.display.update()

        pygame.time.delay(100)

        # Eventos

        # Captura fila de eventos correntes e verifica se houve o estímulo de saída. A fila é esvaziada após o uso do método get
        eventos = pygame.event.get()
        
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)