
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import ImageTk


#Bibliotecas
import math
import numpy as np
import matplotlib.pyplot as plt

# Dicionário para mapear as resoluções
resolucoes = {}
def resolucao(largura, altura, cor_fundo=(0,0,0)):
  # Nome da variável
  resolucao = str(largura)+"X"+str(altura)
  # Verifica se a variável já existe no dicionário, se existir só a retorna, caso contrário a cria
  if not(resolucao in resolucoes):
      resolucoes[resolucao]= np.full((altura, largura, 3), cor_fundo)
  return resolucoes[resolucao]

def deleta_resolucao(largura, altura):
  resolucao = str(largura)+"X"+str(altura)
  if resolucao in resolucoes:
    del resolucoes[resolucao]

def ponto(x, y, pixels, cor):
    """
    Define a cor de um pixel na matriz de pixels.

    :param x: Posição horizontal (coordenada x) do pixel.
    :param y: Posição vertical (coordenada y) do pixel.
    :param cor: Cor do pixel no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente (void).
    """
    pixels[round(y), round(x)] = cor

def reta(x1, y1, x2=None, y2=None, largura = None, altura = None, cor=None):
    """
    Desenha uma reta entre dois pontos na matriz de pixels com a cor especificada.

    :param x1: Coordenada horizontal do primeiro ponto.
    :param y1: Coordenada vertical do primeiro ponto.
    :param x2: Coordenada horizontal do segundo ponto (opcional, padrão igual a x1).
    :param y2: Coordenada vertical do segundo ponto (opcional, padrão igual a y1).
    :param cor: Cor da reta no formato (R, G, B) (opcional, padrão igual a preto).
    :return: Nenhum valor é retornado explicitamente.
    """
    pixels = resolucao(largura, altura)
    # Verifica se x2 e y2 não foram especificados e, se não, define-os como iguais a x1 e y1.

    if x2 is None and y2 is None:
        x2, y2 = x1, y1

    # Transforma os vértices para as dimensões da matriz de pixels.
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

def poligono(vertices, largura, altura, cor):
    """
    Desenha um polígono conectando os vértices na matriz de pixels com a cor especificada e preenche o polígono.

    :param vertices: Uma lista de coordenadas (x, y) dos vértices do polígono.
    :param cor: Cor do polígono no formato (R, G, B).
    :return: Nenhum valor é retornado explicitamente.
    """
    pixels = resolucao(largura, altura)
    num_vertices = len(vertices)

    for i in range(num_vertices):
        # Vértice atual.
        x1, y1 = vertices[i]

        # Próximo vértice. O % faz com que ligue o último vértice ao primeiro.
        x2, y2 = vertices[(i + 1) % num_vertices]

        # Desenha uma reta entre o vértice atual e o próximo vértice.
        reta(x1, y1, x2, y2, largura, altura, cor)

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
                ponto(x, extremidades[y][0], pixels, cor)
                # Avança para a próxima coluna.
                x += 1

# Função para calcular um ponto na curva de Hermite
def calcular_ponto_hermite(curva, t):
    M = np.array([[2, -2, 1, 1],
                  [-3, 3, -2, -1],
                  [0, 0, 1, 0],
                  [1, 0, 0, 0]])
    T = np.array([t**3, t**2, t, 1])
    ponto = T.dot(M).dot(curva)
    return ponto

def rasterizar_curva_hermite(p1x,p1y,p2x,p2y,t1x,t1y,t2x,t2y, num_pontos,largura, altura, cor):
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
        reta(x1, y1, x2, y2,largura, altura, cor)  # Rasteriza o segmento de reta entre os pontos 1 e 2

def plotar_graficos(graficos=None):
  # Cria uma figura vazia
  if graficos is None:
      graficos = resolucoes
  fig = plt.figure(figsize=(15, 5))
  # Itera sobre o dicionário e exibe cada matriz como um gráfico
  for i, (titulo, matriz) in enumerate(graficos.items()):
      # Adicione um subplot para cada gráfico
      ax = fig.add_subplot(1, len(graficos), i + 1)
      ax.set_title(titulo)
      ax.imshow(matriz, cmap='plasma', origin='lower')  # Exibe a matriz como uma imagem

  # Ajusta o layout dos subplots
  plt.tight_layout()
  # Exibe a figura com os gráficos
  plt.show()

def desenhar_reta():
    # Obtenha os valores dos campos p1x, p1y, p2x, p2y, r, g, b, l, e chame a função reta
    p1x = float(p1x_entry.get())
    p1y = float(p1y_entry.get())
    p2x = float(p2x_entry.get())
    p2y = float(p2y_entry.get())
    largura = int(largura_entry.get())
    altura = int(altura_entry.get())
    cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
    reta(p1x, p1y, p2x, p2y, largura, altura, cor)


def plotar():
    print("plotar")
    plotar_graficos()


def desenhar_curva():
    # Obtenha os valores dos campos p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, r, g, b, l,
    # e chame a função rasterizar_curva_hermite
    p1x = float(p1x_entry.get())
    p1y = float(p1y_entry.get())
    p2x = float(p2x_entry.get())
    p2y = float(p2y_entry.get())
    t1x = float(t1x_entry.get())
    t1y = float(t1y_entry.get())
    t2x = float(t2x_entry.get())
    t2y = float(t2y_entry.get())
    num_pontos = int(num_pontos_entry.get())
    cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
    largura = int(largura_entry.get())
    altura = int(altura_entry.get())
    rasterizar_curva_hermite(p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, largura, altura, cor)


def desenhar_poligono():
    # Obtenha os valores dos campos vertices, r, g, b, l, e chame a função poligono
    vertices_str = vertices_entry.get().strip()
    # O formato dos vértices deve ser como: [(x1, y1), (x2, y2), ...]
    vertices = eval(vertices_str)
    cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
    largura = int(largura_entry.get())
    altura = int(altura_entry.get())
    poligono(vertices, largura, altura, cor)


# Crie uma janela principal
janela = tk.Tk()
janela.title("Desenho Gráfico")

# Crie campos de entrada para p1x.
p1x_label = tk.Label(janela, text="P1x:")
p1x_label.grid(row=0, column=0)
p1x_entry = tk.Entry(janela)
p1x_entry.grid(row=0, column=1)

# Crie campos de entrada para p1y.
p1y_label = tk.Label(janela, text="P1y:")
p1y_label.grid(row=0, column=2)
p1y_entry = tk.Entry(janela)
p1y_entry.grid(row=0, column=3)

# Crie campos de entrada para t1x.
t1x_label = tk.Label(janela, text="T1x:")
t1x_label.grid(row=0, column=4)
t1x_entry = tk.Entry(janela)
t1x_entry.grid(row=0, column=5)

# Crie campos de entrada para t1y.
t1y_label = tk.Label(janela, text="T1y:")
t1y_label.grid(row=0, column=6)
t1y_entry = tk.Entry(janela)
t1y_entry.grid(row=0, column=7)

# Crie campos de entrada para p2x.
p2x_label = tk.Label(janela, text="P2x:")
p2x_label.grid(row=1, column=0)
p2x_entry = tk.Entry(janela)
p2x_entry.grid(row=1, column=1)

# Crie campos de entrada para p2y.
p2y_label = tk.Label(janela, text="P2y:")
p2y_label.grid(row=1, column=2)
p2y_entry = tk.Entry(janela)
p2y_entry.grid(row=1, column=3)

# Crie campos de entrada para t2x.
t2x_label = tk.Label(janela, text="T2x:")
t2x_label.grid(row=1, column=4)
t2x_entry = tk.Entry(janela)
t2x_entry.grid(row=1, column=5)

# Crie campos de entrada para t2y.
t2y_label = tk.Label(janela, text="T2y:")
t2y_label.grid(row=1, column=6)
t2y_entry = tk.Entry(janela)
t2y_entry.grid(row=1, column=7)

# Crie campos de entrada para num_pontos.
num_pontos_label = tk.Label(janela, text="nº de pontos:")
num_pontos_label.grid(row=2, column=0)
num_pontos_entry = tk.Entry(janela)
num_pontos_entry.grid(row=2, column=1)

# Crie campos de entrada para r.
r_label = tk.Label(janela, text="R:")
r_label.grid(row=2, column=2)
r_entry = tk.Entry(janela)
r_entry.grid(row=2, column=3)

# Crie campos de entrada para g.
g_label = tk.Label(janela, text="G:")
g_label.grid(row=2, column=4)
g_entry = tk.Entry(janela)
g_entry.grid(row=2, column=5)

# Crie campos de entrada para b.
b_label = tk.Label(janela, text="B:")
b_label.grid(row=2, column=6)
b_entry = tk.Entry(janela)
b_entry.grid(row=2, column=7)

# Crie um campo de entrada para 'vertices'
vertices_label = tk.Label(janela, text="Vertices:")
vertices_label.grid(row=3, column=0)
vertices_entry = tk.Entry(janela)
vertices_entry.grid(row=3, column=1)

# Crie campos de entrada para largura.
largura_label = tk.Label(janela, text="Largura:")
largura_label.grid(row=3, column=2)
largura_entry = tk.Entry(janela)
largura_entry.grid(row=3, column=3)

# Crie campos de entrada para Altura.
altura_label = tk.Label(janela, text="Altura:")
altura_label.grid(row=3, column=4)
altura_entry = tk.Entry(janela)
altura_entry.grid(row=3, column=5)

# Crie botões para desenhar reta, curva e polígono
reta_button = tk.Button(janela, text="Reta", command=desenhar_reta)
reta_button.grid(row=4, column=0)

curva_button = tk.Button(janela, text="Curva", command=desenhar_curva)
curva_button.grid(row=4, column=1)

poligono_button = tk.Button(janela, text="Polígono", command=desenhar_poligono)
poligono_button.grid(row=4, column=2)

exluir_resolucao_button = tk.Button(janela, text="Excluir Resolução", command=desenhar_poligono)
exluir_resolucao_button.grid(row=4, column=3)

plotar_button = tk.Button(janela, text="Plotar", command=plotar)
plotar_button.grid(row=4, column=4)

# Crie uma instância do Figure
fig = Figure(figsize=(5, 4), dpi=100)


# Crie uma janela principal
janela = tk.Tk()
janela.title("Desenho Gráfico")

# Crie campos de entrada, botões e rótulos aqui (como você fez)

# Crie um widget Canvas do Tkinter para incorporar o gráfico
canvas = FigureCanvasTkAgg(fig, master=janela)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Inicie a janela principal
janela.mainloop()