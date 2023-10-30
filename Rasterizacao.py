# Bibliotecas
import math
import numpy as np
import matplotlib.pyplot as plt


def ponto(x, y, pixels, cor):
    """
    Define a cor de um pixel na matriz de pixels.

    :param x: Posição horizontal (coordenada x) do pixel.
    :param y: Posição vertical (coordenada y) do pixel.
    :param cor: Cor do pixel no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente (void).
    """
    pixels[round(y), round(x)] = cor


def reta(x1, y1, x2=None, y2=None, pixels=None, cor=None):
    """
    Desenha uma reta entre dois pontos na matriz de pixels com a cor especificada.

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

    # Normaliza os vértices para as dimensões da matriz de pixels.
    x1 = round((x1 + 1) * (largura - 1) / 2)
    y1 = round((y1 + 1) * (altura - 1) / 2)
    x2 = round((x2 + 1) * (largura - 1) / 2)
    y2 = round((y2 + 1) * (altura - 1) / 2)

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
        fragmento(x1, y1, x2, y2, "x", incremento_x, m, b, pixels, cor)
    else:
        # Caso contrário, rasterize na direção Y.
        if y1 < y2:
            incremento_y = 1
        else:
            incremento_y = -1
        fragmento(x1, y1, x2, y2, "y", incremento_y, m, b, pixels, cor)


def fragmento(x1, y1, x2, y2, eixo_maior_variacao, incremento, m, b, pixels, cor):
    """
    Desenha um fragmento de reta entre dois pontos na matriz de pixels com a cor especificada.

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
    ponto(x, y, pixels, cor)

    if eixo_maior_variacao == "x":
        # Se a maior variação for no eixo X.
        while x != x2:
            x += incremento
            if m != 0:
                y = m * x + b
            ponto(x, y, pixels, cor)
    else:
        # Se a maior variação for no eixo Y.
        while y != y2:
            y += incremento
            if m != 0:
                x = (y - b) / m
            ponto(x, y, pixels, cor)
    plt.title('Reta')


def poligono(vertices, pixels, cor):
    """
    Desenha um polígono conectando os vértices na matriz de pixels com a cor especificada e preenche o polígono.

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
        reta(x1, y1, x2, y2, pixels, cor)

    # Preenche o polígono com a cor especificada.
    preencher(pixels, cor)


def preencher(pixels, cor):
    """
    Preenche uma área delimitada pelo contorno de um polígono com a cor especificada.

    :param pixels: A matriz de pixels onde o preenchimento será aplicado.
    :param cor: A cor do preenchimento no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente.
    """
    # Cria uma lista vazia para armazenar as coordenadas dos pixels que fazem parte do contorno do polígono.
    extremidades = []

    # Obtém as dimensões da matriz de pixels (altura e largura).
    altura = pixels.shape[0]
    largura = pixels.shape[1]

    # Percorre a matriz de pixels para identificar as extremidades do polígono.
    for y in range(altura):
        for x in range(largura):
            # Verifica se a cor do pixel é igual à cor especificada (indicando que faz parte do contorno do polígono).
            if np.array_equal(pixels[y, x], cor):
                # Adiciona as coordenadas do pixel à lista de extremidades.
                extremidades.append((y, x))

    # Preenche o interior do polígono, linha por linha, seguindo as extremidades.
    for y in range(len(extremidades) - 1):
        # Verifica se a linha a ser preenchida é horizontal (mesmo valor de 'y' nos pixels adjacentes).
        if extremidades[y][0] == extremidades[y + 1][0]:
            # Inicia na coluna 'x' do pixel atual.
            x = extremidades[y][1]
            # Preenche a linha até a coluna 'x' do próximo pixel.
            while x < extremidades[y + 1][1]:
                # Define a cor do pixel ao longo da linha como a cor especificada.
                pixels[extremidades[y][0], x] = cor
                # Avança para a próxima coluna.
                x += 1


# Tamanho da matriz de pixels.
largura, altura = 100, 100
# Inicializando uma matriz de zeros para representar os pixels.
cor_fundo = (255, 255, 255)  # Substitua pelos valores iniciais desejados
pixels = np.full((altura, largura, 3), cor_fundo)
# Rasteriza três retas na matriz de pixels.
cor_pixel = (255, 0, 255)
reta(-1, -1, 1, 1, pixels, cor_pixel)
reta(-1, -1, -1, 1, pixels, cor_pixel)
reta(-1, -1, 1, -1, pixels, cor_pixel)
retangulo = [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, - 0.5)]
# Rasterize o polígono.
poligono(retangulo,pixels, (0,255,0))
#Defina os vértices do triângulo.
triangulo = [(0, math.sqrt(3) / 3), (-1 / math.sqrt(3), -1 / 3), (1 / math.sqrt(3), -1 / 3)]
# Rasteriza o triângulo.
poligono(triangulo,pixels, (255,0,0))
# Mostra a imagem
plt.imshow(pixels, cmap='plasma', origin='lower')
plt.show()

# Tamanho da matriz de pixels.
largura, altura = 1920 , 1080
# Inicializando uma matriz de zeros para representar os pixels.
valor_inicial = (0, 0, 0)  # Substitua pelos valores iniciais desejados
pixels = np.full((altura, largura, 3), valor_inicial)
retangulo = [(-0.5, -0.5), (-0.5, 0.5), (0.5, 0.5), (0.5, - 0.5)]
# Rasterize o polígono.
poligono(retangulo,pixels, cor_pixel)
#Defina os vértices do triângulo.
triangulo = [(0, math.sqrt(3) / 3), (-1 / math.sqrt(3), -1 / 3), (1 / math.sqrt(3), -1 / 3)]
# Rasteriza o triângulo.
poligono(triangulo,pixels, (255,0,0))
#Mostra a imagem
plt.title('Triângulo')
plt.imshow(pixels, cmap='plasma', origin='lower')
plt.show()


