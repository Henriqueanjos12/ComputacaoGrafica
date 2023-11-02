# -*- coding: utf-8 -*-

# Bibliotecas
import math
import numpy as np
import matplotlib.pyplot as plt

# Dicionário para mapear as resoluções
resolucoes = {}


def normalizada_para_matriz(x_norm, y_norm, largura, altura):
    x_pixel = round(((x_norm + 1) / 2) * (largura - 1))
    y_pixel = round(((y_norm + 1) / 2) * (altura - 1))
    return x_pixel, y_pixel


def matriz_para_normalizada(x_pixel, y_pixel, largura, altura):
    x_norm = (2 * x_pixel / (largura - 1)) - 1
    y_norm = (2 * y_pixel / (altura - 1)) - 1
    return x_norm, y_norm


def resolucao(largura, altura, cor_fundo=(0, 0, 0)):
    # Nome da variável
    resolucao = str(largura) + "X" + str(altura)
    # Verifica se a variável já existe no dicionário, se existir só a retorna, caso contrário a cria
    if not (resolucao in resolucoes):
        resolucoes[resolucao] = np.full((altura, largura, 3), cor_fundo)
    return resolucoes[resolucao]


def deleta_resolucao(largura, altura):
    resolucao = str(largura) + "X" + str(altura)
    if resolucao in resolucoes:
        del resolucoes[resolucao]


def deleta_tudo():
    resolucoes.clear()


def ponto(x, y, largura, altura, cor):
    pixels = resolucao(largura, altura)
    """
    Define a cor de um pixel na matriz de pixels.

    :param x: Posição horizontal (coordenada x) do pixel.
    :param y: Posição vertical (coordenada y) do pixel.
    :param cor: Cor do pixel no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente (void).
    """
    pixels[round(y), round(x)] = cor


def reta(x1, y1, x2=None, y2=None, largura=None, altura=None, cor=None):
    """
    Desenha uma reta entre dois pontos na matriz de pixels com a cor especificada.

    :param altura:
    :param largura:
    :param x1: Coordenada horizontal do primeiro ponto.
    :param y1: Coordenada vertical do primeiro ponto.
    :param x2: Coordenada horizontal do segundo ponto (opcional, padrão igual a x1).
    :param y2: Coordenada vertical do segundo ponto (opcional, padrão igual a y1).
    :param cor: Cor da reta no formato (R, G, B) (opcional, padrão igual a preto).
    :return: Nenhum valor é retornado explicitamente.
    """
    # Verifica se x2 e y2 não foram especificados e, se não, define-os como iguais a x1 e y1.

    if x2 is None and y2 is None:
        x2, y2 = x1, y1

    # Transforma os vértices para as dimensões da matriz de pixels.
    x1, y1 = normalizada_para_matriz(x1, y1, largura, altura)
    x2, y2 = normalizada_para_matriz(x2, y2, largura, altura)

    # Calcula a variação no eixo X e Y.
    dx = x2 - x1
    dy = y2 - y1

    # Calcula o coeficiente angular (inclinação) da reta.
    if dx != 0:
        m = dy / dx
    else:
        m = 0

    # Calcula o coeficiente linear da reta.
    b = y1 - m * x1

    if abs(dx) > abs(dy):
        # Se a variação em X for maior, rasterize na direção X.
        if x1 < x2:
            incremento_x = 1
        else:
            incremento_x = -1
        fragmento(x1, y1, x2, y2, "x", incremento_x, m, b, largura, altura, cor)
    else:
        # Caso contrário, rasterize na direção Y.
        if y1 < y2:
            incremento_y = 1
        else:
            incremento_y = -1
        fragmento(x1, y1, x2, y2, "y", incremento_y, m, b, largura, altura, cor)


def fragmento(x1, y1, x2, y2, eixo_maior_variacao, incremento, m, b, largura, altura, cor):
    """
    Desenha um fragmento de reta entre dois pontos na matriz de pixels com a cor especificada.

    :param altura:
    :param largura:
    :param x1: Coordenada horizontal do primeiro ponto.
    :param y1: Coordenada vertical do primeiro ponto.
    :param x2: Coordenada horizontal do segundo ponto.
    :param y2: Coordenada vertical do segundo ponto.
    :param eixo_maior_variacao: Indica o eixo com a maior variação (pode ser "x" ou "y").
    :param incremento: Incremento usado para percorrer o fragmento de reta.
    :param m: Coeficiente angular (inclinação) da reta.
    :param b: Coeficiente linear da reta.
    :param cor: Cor do fragmento de reta no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente.
    """
    x = x1
    y = y1

    # Inicia desenhando o ponto inicial do fragmento.
    ponto(x, y, largura, altura, cor)

    if eixo_maior_variacao == "x":
        # Se a maior variação for no eixo X.
        while x != x2:
            x += incremento
            if m != 0:
                y = m * x + b
            ponto(x, y, largura, altura, cor)
    else:
        # Se a maior variação for no eixo Y.
        while y != y2:
            y += incremento
            if m != 0:
                x = (y - b) / m
            ponto(x, y, largura, altura, cor)


def poligono(vertices, largura, altura, cor):
    """
    Desenha um polígono conectando os vértices na matriz de pixels com a cor especificada e preenche o polígono.

    :param largura:
    :param altura:
    :param vertices: Uma lista de coordenadas (x, y) dos vértices do polígono.
    :param cor: Cor do polígono no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente.
    """
    num_vertices = len(vertices)

    for i in range(num_vertices):
        # Vértice atual.
        x1, y1 = vertices[i]

        # Próximo vértice. O % faz com que ligue o último vértice ao primeiro.
        x2, y2 = vertices[(i + 1) % num_vertices]

        # Desenha uma reta entre o vértice atual e o próximo vértice.
        reta(x1, y1, x2, y2, largura, altura, cor)

    # Preenche o polígono com a cor especificada.
    preencher(largura, altura, cor)


def preencher(largura, altura, cor):
    """
    Preenche uma área delimitada pelo contorno de um polígono com a cor especificada.

    :param altura:
    :param largura: A matriz de pixels onde o preenchimento será aplicado.
    :param cor: A cor do preenchimento no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente.
    """
    # Cria uma lista vazia para armazenar as coordenadas dos pixels que fazem parte do contorno do polígono.
    extremidades = []
    pixels = resolucao(largura, altura)

    # Percorre a matriz de pixels para identificar as extremidades do polígono.
    for y in range(altura):
        x_inicio = None  # Coordenada x do primeiro pixel da linha
        x_fim = None  # Coordenada x do último pixel da linha
        for x in range(largura):
            if np.array_equal(pixels[y, x], cor):
                if x_inicio is None:
                    x_inicio = x
                else:
                    x_fim = x
        # Se encontrou o início e o fim da linha
        if x_inicio is not None and x_fim is not None:
            extremidades.append((y, x_inicio))
            extremidades.append((y, x_fim))

    # Preenche o interior do polígono, linha por linha, seguindo as extremidades.
    for i in range(len(extremidades) - 1):
        y0, x0 = extremidades[i]
        y1, x1 = extremidades[i + 1]

        # Converter as coordenadas da matriz de pixels para coordenadas normalizadas
        x0_norm, y0_norm = matriz_para_normalizada(x0, y0, largura, altura)
        x1_norm, y1_norm = matriz_para_normalizada(x1, y1, largura, altura)
        if y0 == y1:
            reta(x0_norm, y0_norm, x1_norm, y1_norm, largura, altura, cor)


# Função para calcular um ponto na curva de Hermite
def calcular_ponto_hermite(curva, t):
    M = np.array([[2, -2, 1, 1],
                  [-3, 3, -2, -1],
                  [0, 0, 1, 0],
                  [1, 0, 0, 0]])
    T = np.array([t ** 3, t ** 2, t, 1])
    ponto = T.dot(M).dot(curva)
    return ponto


def rasterizar_curva_hermite(p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, largura, altura, cor):
    curva = np.array([[p1x, p1y],
                      [p2x, p2y],
                      [t1x, t1y],
                      [t2x, t2y]])
    for j in range(num_pontos - 1):
        t1 = j / (num_pontos - 1)
        t2 = (j + 1) / (num_pontos - 1)

        ponto1 = calcular_ponto_hermite(curva, t1)
        ponto2 = calcular_ponto_hermite(curva, t2)
        x1, y1 = ponto1
        x2, y2 = ponto2
        reta(x1, y1, x2, y2, largura, altura, cor)  # Rasteriza o segmento de reta entre os pontos 1 e 2


def plot_tudo(graficos=None):
    if graficos is None:
        graficos = resolucoes
    # Cria uma figura vazia
    fig = plt.figure()

    # Itera sobre o dicionário e exibe cada matriz como um gráfico
    for i, (titulo, matriz) in enumerate(graficos.items()):
        num_graficos = len(graficos)
        num_colunas = min(2, num_graficos)  # Define o número máximo de colunas como 2
        num_linhas = -(-num_graficos // num_colunas)  # Cálculo para o número de linhas

        # Adicione um subplot para cada gráfico
        ax = fig.add_subplot(num_linhas, num_colunas, i + 1)
        ax.set_title(titulo)
        ax.imshow(matriz, cmap='plasma', origin='lower')  # Exibe a matriz como uma imagem

    return fig


def plot_normalizado(graficos=None):
    if graficos is None:
        graficos = resolucoes
    # Cria uma figura vazia
    fig = plt.figure()

    # Itera sobre o dicionário e exibe cada matriz como um gráfico
    for i, (titulo, matriz) in enumerate(graficos.items()):
        num_graficos = len(graficos)
        num_colunas = min(2, num_graficos)  # Define o número máximo de colunas como 2
        num_linhas = -(-num_graficos // num_colunas)  # Cálculo para o número de linhas

        # Adicione um subplot para cada gráfico
        ax = fig.add_subplot(num_linhas, num_colunas, i + 1)
        ax.set_title(titulo)
        ax.imshow(matriz, cmap='plasma', extent=[-1.0, 1.0, -1.0, 1.0],
                  origin='lower')  # Exibe a matriz como uma imagem

    return fig


def plot_resolucao(largura, altura):
    resolucao = str(largura) + "X" + str(altura)
    if resolucao in resolucoes:
        # Cria uma figura e um eixo
        fig, ax = plt.subplots()
        # Plota a imagem
        ax.imshow(resolucoes[resolucao], origin='lower')
        # Adiciona um título à subplot
        ax.set_title(resolucao)
        # Retorna a figura
        return fig
    else:
        return None


def plot_resolucao_normalizada(largura, altura):
    resolucao = str(largura) + "X" + str(altura)
    if resolucao in resolucoes:
        # Cria uma figura e um eixo
        fig, ax = plt.subplots()
        # Plota a imagem
        ax.imshow(resolucoes[resolucao], extent=[-1.0, 1.0, -1.0, 1.0], origin='lower')
        # Adiciona um título à subplot
        ax.set_title(resolucao)
        # Retorna a figura
        return fig
    else:
        return None


# exemplos
# Resoluções correspondentes a cada subplot
resolucoes_padroes = [(100, 100), (300, 300), (800, 600), (1920, 1080)]
for rp in resolucoes_padroes:
    # Tamanho da matriz de pixels (resolução).
    largura, altura = rp

    # Poligonos
    # Defina os vértices dos polígonos com espaço entre eles.
    triangulo1 = [(-0.8, 0), (-0.4, 0), (-0.6, 0.4)]
    triangulo2 = [(0.2, 0), (0.6, 0), (0.4, 0.4)]
    quadrado1 = [(-0.8, 0.8), (-0.5, 0.8), (-0.5, 0.5), (-0.8, 0.5)]
    quadrado2 = [(0.2, 0.8), (0.5, 0.8), (0.5, 0.5), (0.2, 0.5)]
    hexagono1 = [(-0.7, -0.4), (-0.3, -0.4), (-0.1, -0.6), (-0.3, -0.8), (-0.7, -0.8), (-0.9, -0.6)]
    hexagono2 = [(0.35, -0.6), (0.55, -0.6), (0.65, -0.5), (0.55, -0.4), (0.35, -0.4), (0.25, -0.5)]

    # Rasterize os polígonos.
    poligono(triangulo1, largura, altura, (255, 0, 0))
    poligono(triangulo2, largura, altura, (255, 255, 0))
    poligono(quadrado1, largura, altura, (255, 255, 255))
    poligono(quadrado2, largura, altura, (0, 0, 255))
    poligono(hexagono1, largura, altura, (0, 255, 255))
    poligono(hexagono2, largura, altura, (0, 255, 0))

    cor_pixel = (255, 0, 255)
    # Retas
    # Reta diagonal Crescente
    reta(-1, -1, 1, 1, largura, altura, cor_pixel)
    # Reta diagonal Decrescente
    reta(-1, 1, 1, -1, largura, altura, cor_pixel)
    # Reta Vestical baixo para cima esquerda
    reta(-1, -1, -1, 1, largura, altura, cor_pixel)
    # Reta Vestical cima para baixo direita
    reta(1, 1, 1, -1, largura, altura, cor_pixel)
    # Reta Horizontal esquerda para direita baixo
    reta(-1, -1, 1, -1, largura, altura, cor_pixel)
    # Reta Horizontal direita para esquerda cima
    reta(1, 1, -1, 1, largura, altura, cor_pixel)

    cor_pixel = (0, 0, 255)
    rasterizar_curva_hermite(0, 0, 0.8, -0.4, 0.8, 0.8, -0.3, -1, 100, largura, altura, cor_pixel)
    rasterizar_curva_hermite(0.5, 0.5, 0.5, 0.5, -0.5, -1, 0.5, -1, 100, largura, altura, cor_pixel)
    rasterizar_curva_hermite(-0.5, 0.6, 0.3, 0.6, -0.5, 1, 0.3, -1, 100, largura, altura, cor_pixel)
    rasterizar_curva_hermite(-0.8, 0, -0.4, 0, 2.2, -2, 0, 1.5, 100, largura, altura, cor_pixel)
    rasterizar_curva_hermite(0.7, -0.8, 0.5, -0.4, -2, -0.2, 2, -0.2, 100, largura, altura, cor_pixel)

# Tamanho da matriz de pixels.
largura, altura = 500, 500
retangulo = [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, - 0.5)]
# Rasterize o polígono.
poligono(retangulo, largura, altura, (255, 255, 0))
# Defina os vértices do triângulo.
triangulo = [(0, math.sqrt(3) / 3), (-1 / math.sqrt(3), -1 / 3), (1 / math.sqrt(3), -1 / 3)]
# Rasteriza o triângulo.
poligono(triangulo, largura, altura, (255, 0, 0))
