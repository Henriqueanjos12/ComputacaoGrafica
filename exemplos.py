import math

import numpy as np

import computacao_grafica as cg


# Funções de desenho de formas
def cria_circulo(raio=0.4):
    """
    Cria um círculo com um raio especificado.

    :param raio: Raio do círculo. O valor padrão é 0.4.
    :type raio: float

    :return: Uma lista de coordenadas que representam o círculo.
    :rtype: list of tuple
    """
    # Número de pontos para criar o círculo
    num_pontos = 100

    # Crie o círculo com as coordenadas (x, y)
    theta = np.linspace(0, 2 * np.pi, num_pontos)
    x = raio * np.cos(theta)
    y = raio * np.sin(theta)

    # Coordenadas do círculo azul na escala normalizada
    return list(zip(x, y))


def brasil(largura=5 * 64, altura=5 * 45):
    """
    Desenha as formas da bandeira do Brasil em diferentes resoluções.

    :param largura: Largura da imagem.
    :type largura: int
    :param altura: Altura da imagem.
    :type altura: int
    """
    # Defina os vértices dos polígonos.
    retangulo = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    losango = [(-0.75, 0), (0, 0.75), (0.75, 0), (0, -0.75)]
    circulo = cria_circulo(0.4)
    # Rasterize o polígono.
    cg.poligono(retangulo, largura, altura, (0, 255, 0))
    cg.poligono(losango, largura, altura, (255, 255, 0))
    cg.poligono(circulo, largura, altura, (0, 0, 255))


def minas_gerais(largura=5 * 150, altura=5 * 90):
    """
    Desenha as formas da bandeira de Minas Gerais em diferentes resoluções.

    :param largura: Largura da imagem.
    :type largura: int
    :param altura: Altura da imagem.
    :type altura: int
    """
    retangulo = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
    triangulo = [(0, math.sqrt(3) / 3), (-1 / math.sqrt(3), -1 / 3), (1 / math.sqrt(3), -1 / 3)]
    # Rasteriza o triângulo.
    cg.poligono(retangulo, largura, altura, (255, 255, 255))
    cg.poligono(triangulo, largura, altura, (255, 0, 0))


def exemplos():
    """
    Função de exemplo para desenhar várias formas em diferentes resoluções.
    """
    resolucoes_padroes = [(100, 100),
                          (300, 300),
                          (800, 600),
                          (1920, 1080)]

    for rp in resolucoes_padroes:
        # Tamanho da matriz de pixels (resolução).
        largura, altura = rp

        # Polígonos
        # Defina os vértices dos polígonos com espaço entre eles.
        triangulo1 = [(-0.8, 0), (-0.4, 0), (-0.6, 0.4)]
        triangulo2 = [(0.2, 0), (0.6, 0), (0.4, 0.4)]
        quadrado1 = [(-0.8, 0.8), (-0.5, 0.8), (-0.5, 0.5), (-0.8, 0.5)]
        quadrado2 = [(0.2, 0.8), (0.5, 0.8), (0.5, 0.5), (0.2, 0.5)]
        hexagono1 = [(-0.7, -0.4), (-0.3, -0.4), (-0.1, -0.6), (-0.3, -0.8), (-0.7, -0.8), (-0.9, -0.6)]
        hexagono2 = [(0.35, -0.6), (0.55, -0.6), (0.65, -0.5), (0.55, -0.4), (0.35, -0.4), (0.25, -0.5)]

        # Rasterize os polígonos.
        cg.poligono(triangulo1, largura, altura, (0, 0, 255))
        cg.poligono(triangulo2, largura, altura, (0, 0, 255))
        cg.poligono(quadrado1, largura, altura, (0, 255, 255))
        cg.poligono(quadrado2, largura, altura, (255, 0, 0))
        cg.poligono(hexagono1, largura, altura, (255, 0, 255))
        cg.poligono(hexagono2, largura, altura, (255, 255, 0))

        cor_pixel = (255, 128, 0)
        # Retas
        # Reta diagonal Crescente
        cg.reta(-1, -1, 1, 1, largura, altura, cor_pixel)
        # Reta diagonal Decrescente
        cg.reta(-1, 1, 1, -1, largura, altura, cor_pixel)
        # Reta Vertical baixo para cima esquerda
        cg.reta(-1, -1, -1, 1, largura, altura, cor_pixel)
        # Reta Vertical cima para baixo direita
        cg.reta(1, 1, 1, -1, largura, altura, cor_pixel)
        # Reta Horizontal esquerda para direita baixo
        cg.reta(-1, -1, 1, -1, largura, altura, cor_pixel)
        # Reta Horizontal direita para esquerda cima
        cg.reta(1, 1, -1, 1, largura, altura, cor_pixel)

        cor_pixel = (255, 255, 255)
        # Curvas de Hermite
        cg.curva_hermite(0, 0, 0.8, -0.4, 0.8, 0.8, -0.3, -1, 100, largura, altura, cor_pixel)
        cg.curva_hermite(0.5, 0.5, 0.5, 0.5, -0.5, -1, 0.5, -1, 100, largura, altura, cor_pixel)
        cg.curva_hermite(-0.5, 0.6, 0.3, 0.6, -0.5, 1, 0.3, -1, 100, largura, altura, cor_pixel)
        cg.curva_hermite(-0.8, 0, -0.4, 0, 2.2, -2, 0, 1.5, 100, largura, altura, cor_pixel)
        cg.curva_hermite(0.7, -0.8, 0.5, -0.4, -2, -0.2, 2, -0.2, 100, largura, altura, cor_pixel)

        # Desenhe as formas do Brasil e de Minas Gerais
        brasil()
        minas_gerais()
