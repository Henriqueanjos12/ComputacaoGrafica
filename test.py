import computação_gráfica as cg
import tkinter as tk


def desenhar_reta():
    # Obtenha os valores dos campos p1x, p1y, p2x, p2y, r, g, b, l, e chame a função reta
    p1x = float(p1x_entry.get())
    p1y = float(p1y_entry.get())
    p2x = float(p2x_entry.get())
    p2y = float(p2y_entry.get())
    largura = int(largura_entry.get())
    altura = int(altura_entry.get())
    cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
    cg.reta(p1x, p1y, p2x, p2y, largura, altura, cor)


def plotar():
    print("plotar")
    cg.plotar_graficos()


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
    cg.rasterizar_curva_hermite(p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, largura, altura, cor)


def desenhar_poligono():
    # Obtenha os valores dos campos vertices, r, g, b, l, e chame a função poligono
    vertices_str = vertices_entry.get().strip()
    # O formato dos vértices deve ser como: [(x1, y1), (x2, y2), ...]
    vertices = eval(vertices_str)
    cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
    largura = int(largura_entry.get())
    altura = int(altura_entry.get())
    cg.poligono(vertices, largura, altura, cor)


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

# Crie um widget Canvas do Tkinter para incorporar o gráfico
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Crie um frame para conter o gráfico
frame = tk.Frame(janela)
frame.pack()

# Inicie a janela principal
janela.mainloop()
