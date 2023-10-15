import math

import numpy as np
import matplotlib.pyplot as plt


# Função para ligar um pixel na matriz de pixels.
def liga_pixel(x, y):
    """
    A escolha entre (y, x) e (x, y) nas coordenadas depende da convenção adotada na representação de imagens e
    matrizes em computação. A ordem (y, x) é frequentemente usada para imagens e matrizes, especialmente quando se
    trata de coordenadas 2D, por algumas razões:

    1. Coordenadas Cartesianas: Na matemática e na maioria dos sistemas de computação, as coordenadas seguem a
    convenção cartesiana, onde (x, y) representa uma posição no plano 2D. Nesse sistema, o eixo horizontal (X) é
    geralmente representado primeiro, seguido pelo eixo vertical (Y).

    2. Tradição em Processamento de Imagens: Em processamento de imagens e visão computacional, é comum usar (row,
    column) ou (y, x) para denotar a posição de pixels em uma imagem. A coordenada y representa a linha (ou a
    altura) e a coordenada x representa a coluna (ou a largura) na imagem. Essa convenção é amplamente adotada
    nesse contexto.

    3. Consistência com Linguagens de Programação: Muitas linguagens de programação, como Python com NumPy,
    adotam essa convenção, onde as matrizes são indexadas com base em `(row, column)` ou `(y, x)`.

    No entanto, a ordem (x, y) também é usada em alguns contextos, e isso pode variar dependendo da aplicação ou das
    preferências do desenvolvedor. É importante seguir a convenção apropriada para o contexto em que você está
    trabalhando, a fim de evitar erros e confusões nas coordenadas. No seu código, você usou a ordem (round(y),
    round(x)) para representar as coordenadas dos pixels na matriz, seguindo a convenção comum em processamento de
    imagens.
    :param x: Posição do pixel no eixo x.
    :param y: Posição do pixel no eixo y.
    :return: void
    """
    print(f"Pixel at ({x}, {y})")
    print(f"Pixel at ({round(x)}, {round(y)})")
    pixels[round(y), round(x)] = 1


# Função para rasterizar uma reta de (x1, y1) para (x2, y2).
def rasteriza_reta(x1, y1, x2, y2):
    # Normalizando os vértices
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
        produz_fragmento(x1, y1, x2, y2, "x", incremento_x, m, b)
    else:
        # Caso contrário, rasterize na direção Y.
        if y1 < y2:
            incremento_y = 1
        else:
            incremento_y = -1
        produz_fragmento(x1, y1, x2, y2, "y", incremento_y, m, b)


# Função para produzir fragmentos da reta na matriz de pixels.
def produz_fragmento(x1, y1, x2, y2, eixo_maior_variacao, incremento, m, b):
    x = x1
    y = y1
    if eixo_maior_variacao == "x":
        liga_pixel(x, y)
        while x != x2:
            x += incremento
            if m != 0:
                y = m * x + b
            liga_pixel(x, y)
    else:
        liga_pixel(x, y)
        while y != y2:
            y += incremento
            if m != 0:
                x = (y - b) / m
            liga_pixel(x, y)


def rasteriza_poligono(vertices):
    num_vertices = len(vertices)

    for i in range(num_vertices):
        # Vértice atual.
        x1, y1 = vertices[i]
        # Próximo vértice.
        x2, y2 = vertices[(i + 1) % num_vertices]  # O % faz com que ligue o último vértice ao primeiro.
        rasteriza_reta(x1, y1, x2, y2)


# Tamanho da matriz de pixels.
largura, altura = 100, 100
# Inicializando uma matriz de zeros para representar os pixels.
pixels = np.zeros((altura, largura))
# Rasteriza duas retas na matriz de pixels.
# rasteriza_reta(0, 0, 3, 3)
# rasteriza_reta(0, 0, 0, 6)
# rasteriza_reta(0, 0, 8, 2)
# Defina os vértices do polígono (convexo).
vertices_poligono = [(0, math.sqrt(3) / 3), (-1 / math.sqrt(3), -1 / 3), (1 / math.sqrt(3), -1 / 3)]
print(vertices_poligono)
# Rasterize o polígono.
rasteriza_poligono(vertices_poligono)
# Configura o modo interativo do Matplotlib
plt.ion()
plt.imshow(pixels, cmap='plasma', origin='lower')
# Configurações para exibição da matriz de pixels.
# plt.xticks(np.arange(0.5, largura))
# plt.yticks(np.arange(0.5, altura))
# plt.grid(True, linewidth=1.5, color='black')  # Configurar a largura e a cor do grid
plt.title('Minha Imagem')
plt.show()
vertices_poligono2 = [(-1, -1), (-1, 1), (1, 1), (1, - 1)]
rasteriza_poligono(vertices_poligono2)
plt.imshow(pixels, cmap='plasma', origin='lower')
plt.draw()
# Mantém a janela aberta para interação
plt.ioff()
plt.show()
