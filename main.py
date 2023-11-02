from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import computacao_grafica as cg
import matplotlib
import tkinter as tk
from tkinter import messagebox
import sys

matplotlib.use('TkAgg')  # Substitua 'TkAgg' pelo backend de GUI de sua escolha


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


# Função para criar uma nova janela e exibir a figura
def exibir_figura(figura):
    janela_figura = tk.Toplevel()
    janela_figura.title("Imagem")
    canvas = FigureCanvasTkAgg(figura, master=janela_figura)
    canvas.get_tk_widget().pack()
    canvas.draw()


# Função para exibir uma mensagem de ajuda
def exibir_ajuda():
    mensagem_ajuda = "Bem-vindo à minha aplicação!\n\nVocê pode usar este programa para fazer..."
    messagebox.showinfo("Ajuda", mensagem_ajuda)


def obter_vertices(vertices):
    try:
        # Remove os parênteses e divide os pontos
        pontos = vertices.split('),(')
        # Limpa os parênteses e divide os valores x e y usando obter_componentes
        lista_vertices = [obter_componentes(ponto) for ponto in pontos]
        if len(lista_vertices) >= 3:
            return lista_vertices
        else:
            tk.messagebox.showerror("Vértices Inválidos!", "Um poligono deve ter no mínimo 3 vértices.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Vértices Inválidos!", "Formato inválido. Use (a,b),(c, d),(e,f)...")
        sys.exit()


def obter_num_pontos(num_pontos):
    try:
        num_pontos = int(num_pontos)
        if num_pontos > 0:
            return num_pontos  # Retorna num_pontos
        else:
            messagebox.showerror("Nº de pontos invalido!", "Nº de pontos deve ser positivo.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Nº de pontos invalido!", "Nº de pontos deve ser um inteiro positivo.")
        sys.exit()


def obter_componentes(ponto):
    try:
        # Remove os parênteses e divide os valores
        x, y = map(float, ponto.strip('()').split(','))

        # Verifique se x e y estão no intervalo -1 a 1
        if -1 <= x <= 1 and -1 <= y <= 1:
            return x, y
        else:
            messagebox.showerror("Ponto(s) e/ou Tangente(s) Invalida(s)!",
                                 "Valores de Px, Py, Tx e Ty devem estar no intervalo de -1 a 1.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Ponto(s) e/ou Tangente(s) Invalida(s)!", "Formato inválido. Use (x, y)")
        sys.exit()


def obter_resolucao(resolucao):
    try:
        # Remove os parênteses e divide os valores
        largura, altura = map(int, resolucao.strip('()').split(','))

        # Verifique se largura e altura são inteiros e maiores que zero
        if isinstance(largura, int) and isinstance(altura, int) and largura > 0 and altura > 0:
            return largura, altura
        else:
            messagebox.showerror("Resolução Invalida!", "Largura e altura devem ser números inteiros maiores que zero.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Resolução Invalida!", "Formato inválido. Use (largura, altura)")
        sys.exit()


def obter_cor(rgb):
    try:
        # Remove os parênteses e divide os valores
        r, g, b = map(int, rgb.strip('()').split(','))

        # Verifique se r, g e b são inteiros
        if isinstance(r, int) and isinstance(g, int) and isinstance(b, int):
            # Verifique se r, g e b estão no intervalo de 0 a 255
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                return r, g, b  # Retorna uma tupla com os valores r, g e b
            else:
                messagebox.showerror("Cor Invalida!", "Valores de r, g e b devem estar no intervalo de 0 a 255.")
                sys.exit()
        else:
            messagebox.showerror("Cor Invalida!", "r, g e b devem ser números inteiros.")
            sys.exit()
    except ValueError:
        messagebox.showerror("Cor Invalida!", "Formato inválido. Use (r, g, b)")
        sys.exit()


def reta():
    try:
        # Obtenha os valores dos campos p1x, p1y, p2x, p2y, r, g, b, largura, altura e chame a função reta
        p1x, p1y = obter_componentes(p1_entry.get())
        p2x, p2y = obter_componentes(p2_entry.get())
        largura, altura = obter_resolucao(resolucao_entry.get())
        cor = obter_cor(rgb_entry.get())
        cg.reta(p1x, p1y, p2x, p2y, largura, altura, cor)
        print("Reta criada com sucesso!")
    except:
        sys.stderr.write(f"Reta inválida!, verifique os valores!\n")


def plot_resolucao():
    try:
        largura, altura = obter_resolucao(resolucao_entry.get())
        # Exibe a figura na nova janela
        exibir_figura(cg.plot_resolucao(largura, altura))
        print("Imagem plotada com sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagem!\n")


def plot_resolucao_normalizada():
    try:
        largura, altura = obter_resolucao(resolucao_entry.get())
        # Exibe a figura na nova janela
        exibir_figura(cg.plot_resolucao_normalizada(largura, altura))
        print("Imagem normalizada plotada com Sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagem normalizada!\n")


def plot_tudo():
    try:
        exibir_figura(cg.plot_tudo())
        print("Imagens plotadas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagens!\n")


def plot_normalizado():
    try:
        exibir_figura(cg.plot_normalizado())
        print("Imagens normalizadas plotadas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar Imagens normalizadas!\n")


def curva():
    try:
        # Obtenha os valores dos campos p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, r, g, b, l,
        # e chame a função rasterizar_curva_hermite
        p1x, p1y = obter_componentes(p1_entry.get())
        p2x, p2y = obter_componentes(p2_entry.get())
        t1x, t1y = obter_componentes(t1_entry.get())
        t2x, t2y = obter_componentes(t2_entry.get())
        num_pontos = obter_num_pontos(num_pontos_entry.get())
        cor = obter_cor(rgb_entry.get())
        largura, altura = obter_resolucao(resolucao_entry.get())
        cg.rasterizar_curva_hermite(p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, largura, altura, cor)
        print("Curva adicionada com sucesso!")
    except:
        sys.stderr.write(f"Curva inválida!, verifique os valores!\n")


def poligono():
    try:
        # Obtenha os valores dos campos vertices, r, g, b, l, e chame a função poligono
        vertices = obter_vertices(vertices_entry.get())
        cor = obter_cor(rgb_entry.get())
        largura, altura = obter_resolucao(resolucao_entry.get())
        cg.poligono(vertices, largura, altura, cor)
        print("Polígono criada com sucesso!")
    except:
        sys.stderr.write(f"Polígono inválido!, verifique os valores!\n")


def deleta_resolucao():
    try:
        largura, altura = obter_resolucao(resolucao_entry.get())
        cg.deleta_resolucao(largura, altura)
        print("Resolução deletada com sucesso!")
    except:
        sys.stderr.write(f"Erro ao deletar resolução!\n")


def deleta_tudo():
    try:
        cg.deleta_tudo()
        print("Resoluções deletadas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao deletar todas as resoluções!\n")


# Crie uma janela principal
janela = tk.Tk()
janela.title("Computação Gráfica")

# Definir o tamanho da janela como fixo (largura x altura)
'''largura_janela = 800
altura_janela = 600
janela.geometry(f"{largura_janela}x{altura_janela}")'''
# Impedir que a janela seja redimensionada
janela.resizable(False, False)

# Crie campos de entrada para p1.
p1_label = tk.Label(janela, text="P1:")
p1_label.grid(row=0, column=0, sticky="nsew")
p1_entry = tk.Entry(janela)
p1_entry.grid(row=0, column=1, sticky="nsew")

# Crie campos de entrada para t1.
t1_label = tk.Label(janela, text="T1:")
t1_label.grid(row=0, column=2, sticky="nsew")
t1_entry = tk.Entry(janela)
t1_entry.grid(row=0, column=3, sticky="nsew")

# Crie campos de entrada para p2.
p2_label = tk.Label(janela, text="P2:")
p2_label.grid(row=1, column=0, sticky="nsew")
p2_entry = tk.Entry(janela)
p2_entry.grid(row=1, column=1, sticky="nsew")

# Crie campos de entrada para t2.
t2_label = tk.Label(janela, text="T2:")
t2_label.grid(row=1, column=2, sticky="nsew")
t2_entry = tk.Entry(janela)
t2_entry.grid(row=1, column=3, sticky="nsew")

# Crie campos de entrada para rgb.
rgb_label = tk.Label(janela, text="Cor:")
rgb_label.grid(row=2, column=0, sticky="nsew")
rgb_entry = tk.Entry(janela)
rgb_entry.grid(row=2, column=1, sticky="nsew")

# Crie campos de entrada para resolução.
resolucao_label = tk.Label(janela, text="Resolução:")
resolucao_label.grid(row=2, column=2, sticky="nsew")
resolucao_entry = tk.Entry(janela)
resolucao_entry.grid(row=2, column=3, sticky="nsew")
# Crie campos de entrada para num_pontos.
num_pontos_label = tk.Label(janela, text="Nº de pontos:")
num_pontos_label.grid(row=3, column=0, sticky="nsew")
num_pontos_entry = tk.Entry(janela)
num_pontos_entry.grid(row=3, column=1, sticky="nsew")

# Crie um campo de entrada para 'vertices'
vertices_label = tk.Label(janela, text="Vertices:")
vertices_label.grid(row=3, column=2, sticky="nsew")
vertices_entry = tk.Entry(janela)
vertices_entry.grid(row=3, column=3, sticky="nsew")

# Crie botões para desenhar reta, curva e polígono
reta_button = tk.Button(janela, text="Add Reta", command=reta)
reta_button.grid(row=4, column=0, columnspan=2, sticky="nsew")

curva_button = tk.Button(janela, text="Add Curva", command=curva)
curva_button.grid(row=4, column=2, columnspan=2, sticky="nsew")

poligono_button = tk.Button(janela, text="Add Polígono", command=poligono)
poligono_button.grid(row=4, column=4, columnspan=2, sticky="nsew")

exluir_resolucao_button = tk.Button(janela, text="Excluir Resolução", command=deleta_resolucao)
exluir_resolucao_button.grid(row=2, column=4, sticky="nsew")

exluir_tudo_button = tk.Button(janela, text="Excluir Todas Resoluções", command=deleta_tudo)
exluir_tudo_button.grid(row=2, column=5, columnspan=1, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar Resolução", command=plot_resolucao)
plotar_button.grid(row=0, column=4, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar Resolução Normalizada", command=plot_resolucao_normalizada)
plotar_button.grid(row=1, column=4, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar Tudo", command=plot_tudo)
plotar_button.grid(row=0, column=5, columnspan=1, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar Tudo Normalizado", command=plot_normalizado)
plotar_button.grid(row=1, column=5, columnspan=1, sticky="nsew")

# Criar um botão de ajuda
botao_ajuda = tk.Button(janela, text="Ajuda", command=exibir_ajuda)
botao_ajuda.grid(row=3, column=4, columnspan=2, sticky="nsew")

# Criar um widget de Text para o terminal
terminal = tk.Text(janela, state="disabled", wrap="word")
terminal.grid(row=5, columnspan=6, sticky="nsew")

# Adicionar uma scrollbar ao terminal
scrollbar = tk.Scrollbar(janela, command=terminal.yview)
scrollbar.grid(row=5, column=6, sticky="ns")
terminal["yscrollcommand"] = scrollbar.set

# Adicionar uma tag para o estilo da saída do print
terminal.tag_configure("stdout", foreground="green")
terminal.tag_configure("stderr", foreground="red")

# Redirecionar a saída do print e os erros para o widget de Text
sys.stdout = TextRedirector(terminal, "stdout", sys.stdout)
sys.stderr = TextRedirector(terminal, "stderr", sys.stderr)

# Inicie a janela principal
janela.mainloop()
