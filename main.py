import pygame
import sys
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Super Python Bros")

# Cores
AZUL_CEU = (135, 206, 235)
VERDE = (0, 255, 0)
MARROM = (139, 69, 19)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)

# FPS
relogio = pygame.time.Clock()
FPS = 60

# Gravidade e variáveis de movimento
GRAVIDADE = 0.75
VELOCIDADE_PULO = -15
VELOCIDADE_JOGADOR = 5

# Classes
class Jogador(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cria um retângulo vermelho representando o jogador
        self.image = pygame.Surface((30, 50))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Variáveis de movimento
        self.velocidade_y = 0
        self.velocidade_x = 0
        self.pulando = False
        self.no_chao = False
        self.orientacao = "direita"
        
        # Pontuação
        self.pontos = 0
        
    def movimento(self, plataformas):
        # Movimento horizontal
        self.rect.x += self.velocidade_x
        
        # Verificar colisão horizontal com plataformas
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidade_x > 0:  # Movendo para a direita
                    self.rect.right = plataforma.rect.left
                elif self.velocidade_x < 0:  # Movendo para a esquerda
                    self.rect.left = plataforma.rect.right
        
        # Aplicar gravidade
        self.velocidade_y += GRAVIDADE
        self.rect.y += self.velocidade_y
        
        # Verificar colisão vertical com plataformas
        self.no_chao = False
        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rect):
                if self.velocidade_y > 0:  # Caindo
                    self.rect.bottom = plataforma.rect.top
                    self.velocidade_y = 0
                    self.no_chao = True
                elif self.velocidade_y < 0:  # Subindo (batendo a cabeça)
                    self.rect.top = plataforma.rect.bottom
                    self.velocidade_y = 0
        
        # Limitar o jogador à tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA:
            self.rect.right = LARGURA
        
        # Se cair da tela
        if self.rect.top > ALTURA:
            return "game_over"
        return "jogando"
    
    def pular(self):
        if self.no_chao:
            self.velocidade_y = VELOCIDADE_PULO
            self.no_chao = False
            
    def update(self, plataformas):
        # Lidar com teclas pressionadas
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT]:
            self.velocidade_x = -VELOCIDADE_JOGADOR
            self.orientacao = "esquerda"
        elif teclas[pygame.K_RIGHT]:
            self.velocidade_x = VELOCIDADE_JOGADOR
            self.orientacao = "direita"
        else:
            self.velocidade_x = 0
            
        if teclas[pygame.K_SPACE]:
            self.pular()
            
        # Atualizar a posição do jogador
        return self.movimento(plataformas)

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.image = pygame.Surface((largura, altura))
        self.image.fill(MARROM)
        self.rect = self.image.get_rect(topleft=(x, y))

class Inimigo(pygame.sprite.Sprite):
    def __init__(self, x, y, limite_esquerda, limite_direita):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERDE)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocidade = 2
        self.limite_esquerda = limite_esquerda
        self.limite_direita = limite_direita
        
    def update(self):
        self.rect.x += self.velocidade
        
        if self.rect.right > self.limite_direita or self.rect.left < self.limite_esquerda:
            self.velocidade *= -1

class Moeda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        self.image.fill(AMARELO)
        self.rect = self.image.get_rect(topleft=(x, y))

# Função para criar o nível
def criar_nivel():
    plataformas = pygame.sprite.Group()
    inimigos = pygame.sprite.Group()
    moedas = pygame.sprite.Group()
    
    # Plataforma base (chão)
    plataformas.add(Plataforma(0, ALTURA - 50, LARGURA, 50))
    
    # Plataformas adicionais
    plataformas.add(Plataforma(100, ALTURA - 150, 200, 20))
    plataformas.add(Plataforma(400, ALTURA - 200, 150, 20))
    plataformas.add(Plataforma(600, ALTURA - 250, 200, 20))
    plataformas.add(Plataforma(200, ALTURA - 300, 150, 20))
    plataformas.add(Plataforma(0, ALTURA - 350, 100, 20))
    
    # Criar inimigos
    inimigos.add(Inimigo(150, ALTURA - 180, 100, 280))
    inimigos.add(Inimigo(420, ALTURA - 230, 400, 530))
    inimigos.add(Inimigo(650, ALTURA - 280, 600, 780))
    
    # Adicionar moedas
    for _ in range(15):
        x = random.randint(50, LARGURA - 50)
        y = random.randint(100, ALTURA - 200)
        moedas.add(Moeda(x, y))
    
    return plataformas, inimigos, moedas

# Função para exibir texto
def exibir_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont(None, tamanho)
    superficie = fonte.render(texto, True, cor)
    rect = superficie.get_rect(center=(x, y))
    tela.blit(superficie, rect)

# Função principal do jogo
def jogo():
    # Criar jogador
    jogador = Jogador(50, ALTURA - 150)
    
    # Criar nível
    plataformas, inimigos, moedas = criar_nivel()
    
    estado_jogo = "jogando"
    
    # Loop principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Reiniciar jogo
            if estado_jogo != "jogando" and evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return True  # Reiniciar o jogo
        
        if estado_jogo == "jogando":
            # Limpar a tela
            tela.fill(AZUL_CEU)
            
            # Atualizar jogador
            estado_jogo = jogador.update(plataformas)
            
            # Atualizar inimigos
            inimigos.update()
            
            # Verificar colisão com inimigos
            if pygame.sprite.spritecollide(jogador, inimigos, False):
                estado_jogo = "game_over"
            
            # Verificar colisão com moedas
            moedas_coletadas = pygame.sprite.spritecollide(jogador, moedas, True)
            jogador.pontos += len(moedas_coletadas)
            
            # Verificar vitória
            if len(moedas) == 0:
                estado_jogo = "vitoria"
            
            # Desenhar elementos
            plataformas.draw(tela)
            inimigos.draw(tela)
            moedas.draw(tela)
            tela.blit(jogador.image, jogador.rect)
            
            # Exibir pontuação
            exibir_texto(f"Moedas: {jogador.pontos}", 30, PRETO, 100, 30)
        
        elif estado_jogo == "game_over":
            exibir_texto("GAME OVER", 64, VERMELHO, LARGURA // 2, ALTURA // 2 - 50)
            exibir_texto(f"Pontuação: {jogador.pontos}", 48, PRETO, LARGURA // 2, ALTURA // 2 + 20)
            exibir_texto("Pressione R para jogar novamente", 30, PRETO, LARGURA // 2, ALTURA // 2 + 80)
        
        elif estado_jogo == "vitoria":
            exibir_texto("VOCÊ VENCEU!", 64, AMARELO, LARGURA // 2, ALTURA // 2 - 50)
            exibir_texto(f"Pontuação: {jogador.pontos}", 48, PRETO, LARGURA // 2, ALTURA // 2 + 20)
            exibir_texto("Pressione R para jogar novamente", 30, PRETO, LARGURA // 2, ALTURA // 2 + 80)
        
        # Atualizar a tela
        pygame.display.flip()
        relogio.tick(FPS)
        
    return False

# Iniciar o jogo
if __name__ == "__main__":
    reiniciar = True
    while reiniciar:
        reiniciar = jogo()
    
    pygame.quit()
    sys.exit()