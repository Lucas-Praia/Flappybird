import pygame #biblioteca de criacao de jogos
import os #integra o codigo com os arquivos do computador (imagem)
import random  #geracao de numeros aleatorios, usa para aparecer os canos

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
#pygame.image.load - ele carrega a imagem,
# os.path.join ele pega a imagem na psta que está salva no computador
#pygame.transform.scale2x() - ele aumenta a escala das imagens, porque se for carregado do tamanho que ta na pasta,
# ela fica pequena. Por isso foi usado para aumentar a escala em 2x.

IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))

#O passaro tem 3 imgs, uma com a asa pra cima, outra meio e outra pra baixo, por isso foi criado uma lista.
IMAGEM_PASSARO = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png'))),
]

#criando a fonte da pontuacao do jogo
#pygame.font.init() - inicializa a fonte do jogo
#foi passado para o método Sys.Font duas informacoes. A primeira é a familia da fonte(arial) e a segunda é o tamanho.
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial',50)

#criando as classes do jogo:
class Passaro:
    #variáveis que vai ser passada na criacao do pássaro
    IMGS = IMAGEM_PASSARO
    #animações de rotação (é a parábola que o passaáro faz quando sobe e desce)
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    #de 5 em 5 milisegundos muda a imagem do passaro
    TEMPO_ANIMACAO = 5

    #contruimos o primeiro metodo com o init(posicao: x,y)
    def __init__(self, x, y):
        #atributos do passaro
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        #agora é a funcao que cria o pássaro com a primeira imagem da lista que é a posicao [0]
        self.imagem = self.IMGS[0]

    def pular(self):
        #velocidade negativa para ele poder subir
        self.velocidade = - 10.5
        self.tempo = 0
        #se movimenta no eixo y
        self.altura = self.y

    def mover(self):
    #calcular o deslocamento
        self.tempo += 1
    #1.5 é o valor do tempo da movimentacao dele, pode testar outros valores.
    #fórmula do deslocamento é a do sorvetão--> S= so+vot+at**2/2
        deslocamento = self.velocidade*self.tempo + 1.5 * (self.tempo**2)

    # retringir o deslocamento( para o pássaro nao ir acelerando na queda, ou ir acelerando pra cima disparado)
    #o máximo de deslocamento vai ser 16 pixels.
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
    #quando aperta a barra que o pássaro salta, ele salta de acordo com a fórmula, mas esse deslocamento -=2 está
    # dando um extra no salto que é de 2. Facilita a jogabilidade.
            deslocamento -=2
        self.y += deslocamento

    # o ângulo do pássaro(parábola) --revisar depois q rodar o jogo, experimentar tirando depois do 'or'
        if deslocamento < 0 or self.y < (self.altura+50):
    #se o angulo (quando pular for menor que a rotação máxima, entao o ângulo irá receber a rotação maxima. Deixando
    # o passaro no angulo da rotacao maxima.
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
    #na queda o máximo de ângulo que ele irá ter é -90 graus. Ou seja, se o anglo for maior que -90, o passaro vai
    # ser rotacionado pra baixo(movimento de queda).
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self,tela):
    #definir qual imagem do passaro vai usar
    #quando a contagem da imagem passar do tempo da animacao, muda a imagem.
    #quando a contagem da imagem for menor que 10, entra a segunda imagem
    #quando a contagem for menor que 15, entra a 3 imagem
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

    #se o pássaro tiver caindo, eu nao vou bater asa.
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

    # desenhar a imagem
    #a imagem do passaro vai ser rotacionada
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
    #como se desenhasse um retangulo ao redor da imagem e colasse ele dentro da tela
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x,self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
    #pra desenhar a tela no pygame usa-se (tela.blit)
    #quando ele desenha, qualquer objeto é no topo a esquerda, por isso o top.lef
        tela.blit(imagem_rotacionada,retangulo.topleft)

    #criar a mascara para avaliar a colisao do passaro com o cano
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5
    #altura do cano
    def __init__(self,x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO =  pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self,tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = FONTE_PONTOS.render(f'Pontuação: {pontos}', 1, (255,255,255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    passaros = [Passaro(230,350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
                #keydown - evento de apertar uma tecla do teclado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()
    #mover as coisas
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                #verificando se vai bater no cano e se a altura do passaro for maior q a do cano(vai bater)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)


if __name__ == '__main__':
    main()
