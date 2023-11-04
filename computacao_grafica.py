# -*- coding: utf-8 -*-
# bibliotecas
import sys

import matplotlib.pyplot as plt
import numpy as np

# Dicionário para mapear as resoluções
resolucoes = {}

# Cria uma lista vazia para armazenar as coordenadas dos pixels que fazem parte do contorno do polígono.
extremidades = []


def normalizada_para_matriz(x_norm, y_norm, largura, altura):
    """
    Converte coordenadas normalizadas em coordenadas de matriz.

    :param x_norm: A coordenada x normalizada no intervalo de -1 a 1.
    :type x_norm: float
    :param y_norm: A coordenada y normalizada no intervalo de -1 a 1.
    :type y_norm: float
    :param largura: Largura da matriz na qual deseja mapear as coordenadas normalizadas.
    :type largura: int
    :param altura: Altura da matriz na qual deseja mapear as coordenadas normalizadas.
    :type altura: int

    :return: Um par de coordenadas de matriz (x_pixel, y_pixel) arredondadas para o pixel mais próximo.
    :rtype: tuple
    """
    x_pixel = round(((x_norm + 1) / 2) * (largura - 1))
    y_pixel = round(((y_norm + 1) / 2) * (altura - 1))
    return x_pixel, y_pixel


def matriz_para_normalizada(x_pixel, y_pixel, largura, altura):
    """
    Converte coordenadas de matriz em coordenadas normalizadas.

    :param x_pixel: A coordenada x na matriz.
    :type x_pixel: int
    :param y_pixel: A coordenada y na matriz.
    :type y_pixel: int
    :param largura: Largura da matriz.
    :type largura: int
    :param altura: Altura da matriz.
    :type altura: int

    :return: Um par de coordenadas normalizadas (x_norm, y_norm) no intervalo de -1 a 1.
    :rtype: tuple
    """
    x_norm = (2 * x_pixel / (largura - 1)) - 1
    y_norm = (2 * y_pixel / (altura - 1)) - 1
    return x_norm, y_norm


def resolucao(largura, altura, cor_fundo=(0, 0, 0)):
    """
    Retorna ou cria uma matriz de resolução com uma cor de fundo especificada.

    :param largura: A largura da matriz de resolução.
    :type largura: int
    :param altura: A altura da matriz de resolução.
    :type altura: int
    :param cor_fundo: A cor de fundo da matriz, como uma tupla de 3 elementos (R, G, B).
    :type cor_fundo: tuple, optional
    :return: Uma matriz de resolução com a cor de fundo especificada.
    :rtype: numpy.ndarray
    """
    # Nome da resolução
    nome_resolucao = str(largura) + "X" + str(altura)

    # Verifica se a resolução já existe no dicionário, se existir só a retorna, caso contrário a cria
    if not (nome_resolucao in resolucoes):
        resolucoes[nome_resolucao] = np.full((altura, largura, 3), cor_fundo)

    return resolucoes[nome_resolucao]


def deleta_resolucao(largura, altura):
    """
    Remove uma matriz de resolução com base na largura e altura especificadas, se existir.

    :param largura: A largura da matriz de resolução a ser removida.
    :type largura: int
    :param altura: A altura da matriz de resolução a ser removida.
    :type altura: int
    """
    resolucao_para_apagar = str(largura) + "X" + str(altura)

    if resolucao_para_apagar in resolucoes:
        del resolucoes[resolucao_para_apagar]


def deleta_tudo():
    """
    Remove todas as matrizes de resolução existentes, limpando o dicionário de resoluções.
    """
    resolucoes.clear()


def ponto(x, y, largura, altura, cor, ehpoligono=False):
    """
    Define a cor de um pixel na matriz de pixels.

    :param x: Posição horizontal (coordenada x) do pixel.
    :type x: float
    :param y: Posição vertical (coordenada y) do pixel.
    :type y: float
    :param largura: Largura da matriz de pixels.
    :type largura: int
    :param altura: Altura da matriz de pixels.
    :type altura: int
    :param cor: Cor do pixel no formato (R, G, B).
    :type cor: tuple
    :param ehpoligono: Indica se o ponto faz parte de um polígono (opcional).
    :type ehpoligono: bool
    :return: Nenhum valor é retornado explicitamente (void).
    """
    pixels = resolucao(largura, altura)
    if ehpoligono:
        extremidades.append((round(y), round(x)))
    pixels[round(y), round(x)] = cor


def reta(x1, y1, x2=None, y2=None, largura=None, altura=None, cor=None, ehpoligono=False):
    """
    Desenha uma reta entre dois pontos na matriz de pixels com a cor especificada.

    :param x1: Coordenada horizontal do primeiro ponto.
    :type x1: float
    :param y1: Coordenada vertical do primeiro ponto.
    :type y1: float
    :param x2: Coordenada horizontal do segundo ponto (opcional, padrão igual a x1).
    :type x2: float
    :param y2: Coordenada vertical do segundo ponto (opcional, padrão igual a y1).
    :type y2: float
    :param largura: Largura da matriz de pixels.
    :type largura: int
    :param altura: Altura da matriz de pixels.
    :type altura: int
    :param cor: Cor da reta no formato (R, G, B) (opcional, padrão é None para usar a cor atual).
    :type cor: tuple
    :param ehpoligono: Indica se a reta faz parte de um polígono (opcional, padrão é False).
    :type ehpoligono: bool
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
        fragmento(x1, y1, x2, y2, "x", incremento_x, m, b, largura, altura, cor, ehpoligono)
    else:
        # Caso contrário, rasterize na direção Y.
        if y1 < y2:
            incremento_y = 1
        else:
            incremento_y = -1
        fragmento(x1, y1, x2, y2, "y", incremento_y, m, b, largura, altura, cor, ehpoligono)


def fragmento(x1, y1, x2, y2, eixo_maior_variacao, incremento, m, b, largura, altura, cor, ehpoligono=False):
    """
    Desenha um fragmento de reta entre dois pontos na matriz de pixels com a cor especificada.

    :param altura: A altura da matriz de pixels.
    :type altura: int
    :param largura: A largura da matriz de pixels.
    :type largura: int
    :param x1: Coordenada horizontal do primeiro ponto.
    :type x1: int
    :param y1: Coordenada vertical do primeiro ponto.
    :type y1: int
    :param x2: Coordenada horizontal do segundo ponto.
    :type x2: int
    :param y2: Coordenada vertical do segundo ponto.
    :type y2: int
    :param eixo_maior_variacao: Indica o eixo com a maior variação (pode ser "x" ou "y").
    :type eixo_maior_variacao: str
    :param incremento: Incremento usado para percorrer o fragmento de reta.
    :type incremento: int
    :param m: Coeficiente angular (inclinação) da reta.
    :type m: float
    :param b: Coeficiente linear da reta.
    :type b: float
    :param cor: Cor do fragmento de reta no formato (R, G, B).
    :type cor: tuple
    :param ehpoligono: Indica se o fragmento de reta faz parte de um polígono (opcional, padrão é False).
    :type ehpoligono: bool
    :return: Nenhum valor é retornado explicitamente.
    """
    x = x1
    y = y1

    # Inicia desenhando o ponto inicial do fragmento.
    ponto(x, y, largura, altura, cor, ehpoligono)

    if eixo_maior_variacao == "x":
        # Se a maior variação for no eixo X.
        while x != x2:
            x += incremento
            if m != 0:
                y = m * x + b
            ponto(x, y, largura, altura, cor, ehpoligono)
    else:
        # Se a maior variação for no eixo Y.
        while y != y2:
            y += incremento
            if m != 0:
                x = (y - b) / m
            ponto(x, y, largura, altura, cor, ehpoligono)


def poligono(vertices, largura, altura, cor):
    """
    Desenha um polígono conectando os vértices na matriz de pixels com a cor especificada e preenche o polígono.

    :param vertices: Uma lista de coordenadas (x, y) dos vértices do polígono.
    :type vertices: list
    :param largura: Largura da matriz de pixels.
    :type largura: int
    :param altura: Altura da matriz de pixels.
    :type altura: int
    :param cor: Cor do polígono no formato (R, G, B).
    :type cor: tuple
    :return: Nenhum valor é retornado explicitamente.
    """
    # Esvazia a lista de extremidades
    extremidades.clear()
    num_vertices = len(vertices)
    for i in range(num_vertices):
        # Vértice atual.
        x1, y1 = vertices[i]

        # Próximo vértice. O % faz com que ligue o último vértice ao primeiro.
        x2, y2 = vertices[(i + 1) % num_vertices]

        # Desenha uma reta entre o vértice atual e o próximo vértice.
        reta(x1, y1, x2, y2, largura, altura, cor, True)

    # Preenche o polígono com a cor especificada.
    preencher(largura, altura, cor)


def preencher(largura, altura, cor):
    """
    Preenche uma área delimitada pelo contorno de um polígono com a cor especificada.

    :param largura: A largura da matriz de pixels onde o preenchimento será aplicado.
    :type largura: int
    :param altura: A altura da matriz de pixels onde o preenchimento será aplicado.
    :type altura: int
    :param cor: A cor do preenchimento no formato (R, G, B).
    :type cor: tuple
    :return: Nenhum valor é retornado explicitamente.
    """
    # ordena os pixels de extremidade, juntando todos da mesma linha!
    extremidades.sort()
    # Preenche o interior do polígono, linha por linha, seguindo as extremidades.
    for i in range(len(extremidades) - 1):
        y0, x0 = extremidades[i]
        y1, x1 = extremidades[i + 1]
        # Converter as coordenadas da matriz de pixels para coordenadas normalizadas
        x0_norm, y0_norm = matriz_para_normalizada(x0, y0, largura, altura)
        x1_norm, y1_norm = matriz_para_normalizada(x1, y1, largura, altura)
        if y0 == y1:
            reta(x0_norm, y0_norm, x1_norm, y1_norm, largura, altura, cor)


def calcular_ponto_hermite(curva, t):
    """
    Calcula um ponto na curva de Hermite no parâmetro t.

    Esta função calcula um ponto na curva de Hermite usando os parâmetros da curva e o valor do parâmetro t.

    :param curva: Uma matriz (numpy array) que representa os pontos de controle da curva de Hermite.
    :type curva: numpy.ndarray
    :param t: O valor do parâmetro t na curva de Hermite.
    :type t: float
    :return: Um ponto na curva de Hermite no parâmetro t.
    :rtype: numpy.ndarray
    """
    matriz_hermite = np.array([[2, -2, 1, 1],
                               [-3, 3, -2, -1],
                               [0, 0, 1, 0],
                               [1, 0, 0, 0]])
    matriz_t = np.array([t ** 3, t ** 2, t, 1])
    ponto_curva = matriz_t.dot(matriz_hermite).dot(curva)
    return ponto_curva


def curva_hermite(p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, largura, altura, cor):
    """
    Rasteriza uma curva de Hermite usando pontos de controle e seus pontos tangentes.

    Esta função rasteriza uma curva de Hermite usando os pontos de controle, os pontos tangentes, e gera um número
    especificado de pontos intermediários na curva, desenhados como segmentos de reta.

    :param p1x: Coordenada x do primeiro ponto de controle.
    :type p1x: float
    :param p1y: Coordenada y do primeiro ponto de controle.
    :type p1y: float
    :param p2x: Coordenada x do segundo ponto de controle.
    :type p2x: float
    :param p2y: Coordenada y do segundo ponto de controle.
    :type p2y: float
    :param t1x: Coordenada x do primeiro ponto tangente.
    :type t1x: float
    :param t1y: Coordenada y do primeiro ponto tangente.
    :type t1y: float
    :param t2x: Coordenada x do segundo ponto tangente.
    :type t2x: float
    :param t2y: Coordenada y do segundo ponto tangente.
    :type t2y: float
    :param num_pontos: O número de pontos intermediários a serem gerados na curva.
    :type num_pontos: int
    :param largura: Largura da matriz de pixels.
    :type largura: int
    :param altura: Altura da matriz de pixels.
    :type altura: int
    :param cor: Cor dos segmentos de reta a serem desenhados.
    :type cor: tuple
    :return: Nenhum valor é retornado explicitamente.
    """
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
        if -1 <= x1 <= 1 and -1 <= y1 <= 1 and -1 <= x2 <= 1 and -1 <= y2 <= 1:
            reta(x1, y1, x2, y2, largura, altura, cor)  # Rasteriza o segmento de reta entre os pontos 1 e 2
        else:
            sys.stderr.write(
                f"Curva com pontos fora do espaço normalizado!\n P1: {tuple(ponto1)} e P2: {tuple(ponto2)}\n")


def plot_tudo(graficos=None):
    """
    Plota gráficos a partir de um dicionário de resoluções.

    Esta função cria uma figura vazia e plota gráficos a partir de um dicionário de resoluções. Se nenhum dicionário
    for especificado, ela usará o dicionário de resoluções padrão.

    :param graficos: Um dicionário de resoluções onde as imagens serão obtidas para plotagem (opcional).
    :type graficos: dict
    :return: Nenhum valor é retornado explicitamente, mas a figura é exibida.
    """
    if graficos is None:
        graficos = resolucoes
    # Cria uma figura vazia
    fig = plt.figure()
    # Adicione o código aqui para plotar os gráficos usando a biblioteca matplotlib

    # Itera sobre o dicionário e exibe cada matriz como um gráfico
    for i, (titulo, matriz) in enumerate(graficos.items()):
        num_graficos = len(graficos)
        num_colunas = min(2, num_graficos)  # Define o número máximo de colunas como 2
        num_linhas = -(-num_graficos // num_colunas)  # Cálculo para o número de linhas

        # Adicione um subplot para cada gráfico
        ax = fig.add_subplot(num_linhas, num_colunas, i + 1)
        ax.set_title(titulo)
        ax.imshow(matriz, cmap='plasma', origin='lower')  # Exibe a matriz como uma imagem
    # Ajusta o layout dos subplots
    fig.tight_layout()
    # Adiciona um título geral às subplots
    plt.suptitle('Todas Resoluções')
    # Ative o modo interativo
    plt.ion()
    # Exibe a figura com os gráficos
    plt.show()


def plot_tudo_normalizado(graficos=None):
    """
    Plota gráficos a partir de um dicionário de resoluções normalizadas.

    Esta função cria uma figura vazia e plota gráficos a partir de um dicionário de resoluções normalizadas. Se nenhum
    dicionário for especificado, ela usará o dicionário de resoluções padrão.

    :param graficos: Um dicionário de resoluções normalizadas onde as imagens serão obtidas para plotagem (opcional).
    :type graficos: dict
    :return: Nenhum valor é retornado explicitamente, mas a figura com os gráficos é exibida.
    """
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

    # Ajusta o layout dos subplots
    fig.tight_layout()
    # Adiciona um título geral às subplots
    plt.suptitle('Todas Resoluções Normalizadas')
    # Ative o modo interativo
    plt.ion()
    # Exibe a figura com os gráficos
    plt.show()


def plot_resolucao(largura, altura):
    """
    Plota uma resolução específica a partir de um dicionário de resoluções.

    Esta função cria uma figura vazia e plota a imagem correspondente à resolução especificada a partir de um dicionário
    de resoluções. Se a resolução não for encontrada no dicionário, nada será plotado.

    :param largura: A largura da resolução a ser plotada.
    :type largura: int
    :param altura: A altura da resolução a ser plotada.
    :type altura: int
    :return: Nenhum valor é retornado explicitamente, mas a figura com a resolução é exibida se encontrada.
    """
    resolucao_para_plotar = str(largura) + "X" + str(altura)
    # Cria uma figura vazia
    fig = plt.figure()
    if resolucao_para_plotar in resolucoes:
        # Adicione um subplot para a resolução
        ax = fig.add_subplot()
        # Plota a imagem
        ax.imshow(resolucoes[resolucao_para_plotar], origin='lower')
        # Adiciona um título à subplot
        ax.set_title(resolucao_para_plotar)
    # Ajusta o layout da subplot
    fig.tight_layout()
    # Adiciona um título geral à subplot
    plt.suptitle('Resolução')
    # Ative o modo interativo
    plt.ion()
    # Exibe a figura com a resolução, se encontrada
    plt.show()


def plot_resolucao_normalizada(largura, altura):
    """
    Plota uma resolução normalizada específica a partir de um dicionário de resoluções normalizadas.

    Esta função cria uma figura vazia e plota a imagem correspondente à resolução normalizada especificada a partir de
    um dicionário de resoluções normalizadas. Se a resolução não for encontrada no dicionário, nada será plotado.

    :param largura: A largura da resolução normalizada a ser plotada.
    :type largura: int
    :param altura: A altura da resolução normalizada a ser plotada.
    :type altura: int
    :return: Nenhum valor é retornado explicitamente, mas a figura com a resolução normalizada é exibida se encontrada.
    """
    resolucao_para_plotar_normalizada = str(largura) + "X" + str(altura)
    # Cria uma figura vazia
    fig = plt.figure()
    if resolucao_para_plotar_normalizada in resolucoes:
        # Adicione um subplot para a resolução normalizada
        ax = fig.add_subplot()
        # Plota a imagem
        ax.imshow(resolucoes[resolucao_para_plotar_normalizada], extent=[-1.0, 1.0, -1.0, 1.0], origin='lower')
        # Adiciona um título à subplot
        ax.set_title(resolucao_para_plotar_normalizada)
    # Ajusta o layout da subplot
    fig.tight_layout()
    # Adiciona um título geral à subplot
    plt.suptitle('Resolução Normalizada')
    # Ative o modo interativo
    plt.ion()
    # Exibe a figura com a resolução normalizada, se encontrada
    plt.show()
