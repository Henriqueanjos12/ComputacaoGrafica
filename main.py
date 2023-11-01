import computacao_grafica as cg
import matplotlib

matplotlib.use('TkAgg')  # Substitua 'TkAgg' pelo backend de GUI de sua escolha
import matplotlib.pyplot as plt
import tkinter as tk
import sys


class TextRedirector:
    def __init__(self, widget, tag, stream):
        self.widget = widget
        self.tag = tag
        self.stream = stream

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text, (self.tag,))
        self.widget.configure(state="disabled")
        self.stream.write(text)


def reta():
    try:
        # Obtenha os valores dos campos p1x, p1y, p2x, p2y, r, g, b, largura, altura e chame a função reta
        p1x = float(p1x_entry.get())
        p1y = float(p1y_entry.get())
        p2x = float(p2x_entry.get())
        p2y = float(p2y_entry.get())
        largura = int(largura_entry.get())
        altura = int(altura_entry.get())
        cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
        cg.reta(p1x, p1y, p2x, p2y, largura, altura, cor)
        print("Reta criada com sucesso!")
    except:
        sys.stderr.write(f"Erro, verifique os valores!\n")


def plotar():
    try:
        cg.plotar_imagens()
        print("Imagens plotadas com Sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagens!\n")


def plotar_normalizado():
    try:
        cg.plot_normalizado()
        print("Imagens normalizadas plotadas com Sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar Imagens normalizadas!\n")


def curva():
    try:
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
        print("Curva criada com sucesso!")
    except:
        sys.stderr.write(f"Erro, verifique os valores!\n")


def poligono():
    try:
        # Obtenha os valores dos campos vertices, r, g, b, l, e chame a função poligono
        vertices_str = vertices_entry.get().strip()
        # O formato dos vértices deve ser como: [(x1, y1), (x2, y2), ...]
        vertices = eval(vertices_str)
        cor = (int(r_entry.get()), int(g_entry.get()), int(b_entry.get()))
        largura = int(largura_entry.get())
        altura = int(altura_entry.get())
        cg.poligono(vertices, largura, altura, cor)
        print("Polígono criada com sucesso!")
    except:
        sys.stderr.write(f"Erro, verifique os valores!\n")


def deleta_resolucao():
    try:
        largura = int(largura_entry.get())
        altura = int(altura_entry.get())
        cg.deleta_resolucao(largura, altura)
        print("Resolução deletada com sucesso!")
    except:
        sys.stderr.write(f"Erro ao deletar resolução!\n")


def deleta_tudo():
    try:
        cg.deleta_tudo()
        print("Resoluções deletadas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao deletar as resoluções!\n")


# Crie uma janela principal
janela = tk.Tk()
janela.title("Computação Gráfica")

# Definir o tamanho da janela como fixo (largura x altura)
largura_janela = 800
altura_janela = 600
janela.geometry(f"{largura_janela}x{altura_janela}")
# Impedir que a janela seja redimensionada
janela.resizable(False, False)

# Crie campos de entrada para p1x.
p1x_label = tk.Label(janela, text="P1x:")
p1x_label.grid(row=0, column=0, sticky="nsew")
p1x_entry = tk.Entry(janela)
p1x_entry.grid(row=0, column=1, sticky="nsew")

# Crie campos de entrada para p1y.
p1y_label = tk.Label(janela, text="P1y:")
p1y_label.grid(row=0, column=2, sticky="nsew")
p1y_entry = tk.Entry(janela)
p1y_entry.grid(row=0, column=3, sticky="nsew")

# Crie campos de entrada para t1x.
t1x_label = tk.Label(janela, text="T1x:")
t1x_label.grid(row=0, column=4, sticky="nsew")
t1x_entry = tk.Entry(janela)
t1x_entry.grid(row=0, column=5, sticky="nsew")

# Crie campos de entrada para t1y.
t1y_label = tk.Label(janela, text="T1y:")
t1y_label.grid(row=0, column=6, sticky="nsew")
t1y_entry = tk.Entry(janela)
t1y_entry.grid(row=0, column=7, sticky="nsew")

# Crie campos de entrada para p2x.
p2x_label = tk.Label(janela, text="P2x:")
p2x_label.grid(row=1, column=0, sticky="nsew")
p2x_entry = tk.Entry(janela)
p2x_entry.grid(row=1, column=1, sticky="nsew")

# Crie campos de entrada para p2y.
p2y_label = tk.Label(janela, text="P2y:")
p2y_label.grid(row=1, column=2, sticky="nsew")
p2y_entry = tk.Entry(janela)
p2y_entry.grid(row=1, column=3, sticky="nsew")

# Crie campos de entrada para t2x.
t2x_label = tk.Label(janela, text="T2x:")
t2x_label.grid(row=1, column=4, sticky="nsew")
t2x_entry = tk.Entry(janela)
t2x_entry.grid(row=1, column=5, sticky="nsew")

# Crie campos de entrada para t2y.
t2y_label = tk.Label(janela, text="T2y:")
t2y_label.grid(row=1, column=6, sticky="nsew")
t2y_entry = tk.Entry(janela)
t2y_entry.grid(row=1, column=7, sticky="nsew")

# Crie campos de entrada para num_pontos.
num_pontos_label = tk.Label(janela, text="nº de pontos:")
num_pontos_label.grid(row=2, column=0, sticky="nsew")
num_pontos_entry = tk.Entry(janela)
num_pontos_entry.grid(row=2, column=1, sticky="nsew")

# Crie campos de entrada para r.
r_label = tk.Label(janela, text="R:")
r_label.grid(row=2, column=2, sticky="nsew")
r_entry = tk.Entry(janela)
r_entry.grid(row=2, column=3, sticky="nsew")

# Crie campos de entrada para g.
g_label = tk.Label(janela, text="G:")
g_label.grid(row=2, column=4, sticky="nsew")
g_entry = tk.Entry(janela)
g_entry.grid(row=2, column=5, sticky="nsew")

# Crie campos de entrada para b.
b_label = tk.Label(janela, text="B:")
b_label.grid(row=2, column=6, sticky="nsew")
b_entry = tk.Entry(janela)
b_entry.grid(row=2, column=7, sticky="nsew")

# Crie um campo de entrada para 'vertices'
vertices_label = tk.Label(janela, text="Vertices:")
vertices_label.grid(row=3, column=0, sticky="nsew")
vertices_entry = tk.Entry(janela)
vertices_entry.grid(row=3, column=1, sticky="nsew")

# Crie campos de entrada para largura.
largura_label = tk.Label(janela, text="Largura:")
largura_label.grid(row=3, column=2, sticky="nsew")
largura_entry = tk.Entry(janela)
largura_entry.grid(row=3, column=3, sticky="nsew")

# Crie campos de entrada para Altura.
altura_label = tk.Label(janela, text="Altura:")
altura_label.grid(row=3, column=4, sticky="nsew")
altura_entry = tk.Entry(janela)
altura_entry.grid(row=3, column=5, sticky="nsew")

# Crie botões para desenhar reta, curva e polígono
reta_button = tk.Button(janela, text="Reta", command=reta)
reta_button.grid(row=4, column=0, sticky="nsew")

curva_button = tk.Button(janela, text="Curva", command=curva)
curva_button.grid(row=4, column=1, sticky="nsew")

poligono_button = tk.Button(janela, text="Polígono", command=poligono)
poligono_button.grid(row=4, column=2, sticky="nsew")

exluir_resolucao_button = tk.Button(janela, text="Excluir Resolução", command=deleta_resolucao)
exluir_resolucao_button.grid(row=4, column=3, sticky="nsew")

exluir_tudo_button = tk.Button(janela, text="Excluir Todas Resolução", command=deleta_tudo)
exluir_tudo_button.grid(row=4, column=4, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar Normalizado", command=plotar_normalizado)
plotar_button.grid(row=4, column=5, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar", command=plotar)
plotar_button.grid(row=4, column=6, sticky="nsew")

# Criar um widget de Text para o terminal
terminal = tk.Text(janela, state="disabled", wrap="word")
terminal.grid(row=5, columnspan=7, sticky="nsew")

# Adicionar uma scrollbar ao terminal
scrollbar = tk.Scrollbar(janela, command=terminal.yview)
scrollbar.grid(row=5, column=7, sticky="ns")
terminal["yscrollcommand"] = scrollbar.set

# Adicionar uma tag para o estilo da saída do print
terminal.tag_configure("stdout", foreground="green")
terminal.tag_configure("stderr", foreground="red")

# Redirecionar a saída do print e os erros para o widget de Text
sys.stdout = TextRedirector(terminal, "stdout", sys.stdout)
sys.stderr = TextRedirector(terminal, "stderr", sys.stderr)

# Inicie a janela principal
janela.mainloop()
