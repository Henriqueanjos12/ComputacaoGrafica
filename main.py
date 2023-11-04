import sys
import tkinter as tk
from tkinter import messagebox

import matplotlib

import computacao_grafica as cg
import exemplos as ex

matplotlib.use('TkAgg')


class TextRedirector:
    """
    Redireciona a saída de texto para um widget em uma interface gráfica.

    Esta classe permite redirecionar a saída de texto para um widget de texto em uma interface gráfica, como parte do
    controle de saída de texto para um aplicativo gráfico.

    :param widget: O widget de texto para o qual a saída será redirecionada.
    :type widget: tk.Text
    :param tag: A tag para aplicar ao texto redirecionado (opcional).
    :type tag: str
    :param stream: O objeto stream de saída a ser redirecionado (pode ser sys.stdout, sys.stderr, etc.).
    :type stream: object
    """

    def __init__(self, widget, tag, stream):
        self.widget = widget
        self.tag = tag
        self.stream = stream

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("end", text, (self.tag,))
        self.widget.configure(state="disabled")
        self.stream.write(text)


def exemplos():
    """
    Executa a criação de exemplos.

    Esta função chama a função 'ex.exemplos()' para criar exemplos e imprime uma mensagem de sucesso ou erro, dependendo
    do resultado. Caso a função 'ex.exemplos()' levante uma exceção, uma mensagem de erro será exibida.

    :return: Nenhum valor é retornado explicitamente.
    """
    try:
        ex.exemplos()
        print("Exemplos criados com sucesso!")
    except Exception as e:
        sys.stderr.write(f"Exemplos inválidos, tente novamente!\nErro: {e}\n")


def exibir_ajuda():
    """
    Exibe instruções de uso da interface de Computação Gráfica.

    Esta função exibe instruções de uso para a interface de Computação Gráfica, descrevendo como usar as diferentes
    funcionalidades disponíveis.

    :return: Nenhum valor é retornado explicitamente.
    """
    try:
        mensagem_ajuda = """
        Bem-vindo à Interface de Computação Gráfica!

        Instruções de Uso:

        1. Reta:
           - Preencha os campos P1 e P2 com as coordenadas dos pontos inicial e final da reta (por exemplo, P1: (0.2, 0.3), P2: (0.8, 0.9)).
           - Especifique a cor em formato RGB nos campos de Cor (por exemplo, Cor: (255, 0, 0) para vermelho).
           - Insira a resolução da imagem no campo Resolução (por exemplo, Resolução: (800, 600)).
           - Clique em "Add Reta" para desenhar a reta.

        2. Curva Hermite:
           - Preencha os campos P1 e P2 com as coordenadas dos pontos inicial e final da curva (por exemplo, P1: (0.2, 0.3), P2: (0.8, 0.9)).
           - Preencha os campos T1 e T2 com os vetores tangentes em P1 e P2 (por exemplo, T1: (0.5, 0.0), T2: (-0.5, 0.0)).
           - Especifique a cor em formato RGB nos campos de Cor (por exemplo, Cor: (0, 255, 0) para verde).
           - Insira a resolução da imagem no campo Resolução (por exemplo, Resolução: (300, 300)).
           - Especifique o número de pontos para rasterização no campo Nº de pontos.
           - Clique em "Add Curva" para desenhar a curva de Hermite.

        3. Polígono:
           - Preencha o campo Vertices com as coordenadas dos vértices do polígono, separados por vírgulas e entre parênteses(por exemplo, Vertices: (0.2, 0.3), (0.5, 0.6), (0.8, 0.9)).
           - Especifique a cor em formato RGB nos campos de Cor (por exemplo, Cor: (0, 0, 255) para azul).
           - Insira a resolução da imagem no campo Resolução (por exemplo, Resolução: (1920, 1080)).
           - Clique em "Add Polígono" para desenhar o polígono.

        4. Excluir Resolução:
           - Preencha o campo Resolução com a resolução que deseja excluir e clique em "Excluir Resolução" para remover a imagem correspondente.

        5. Excluir Todas Resoluções:
           - Clique em "Excluir Todas Resoluções" para remover todas as imagens plotadas.

        6. Plotar Resolução:
           - Preencha o campo Resolução e clique em "Plotar Resolução" para exibir a imagem da resolução especificada.

        7. Plotar Resolução Normalizada:
           - Preencha o campo Resolução e clique em "Plotar Resolução Normalizada" para exibir a imagem normalizada, -1 a 1, da resolução especificada.

        8. Plotar Todas Resoluções:
           - Clique em "Plotar Todas Resoluções" para exibir todas as imagens plotadas na interface.

        9. Plotar Todas Resoluções Normalizado:
           - Clique em "Plotar Todas Resoluções Normalizado" para exibir todas as imagens normalizadas, -1 a 1, plotadas na interface.

        10. Exemplos:
           - Clique em "Exemplos" para criar exemplos predefinidos para fins de demonstração.

        11. Ajuda:
           - Clique em "Ajuda" para exibir estas instruções de uso novamente.

        Certifique-se de inserir os valores corretamente e clique nos botões correspondentes para executar as ações desejadas.
        """
        messagebox.showinfo("Ajuda", mensagem_ajuda)
        print("Ajuda exibida com sucesso!")
    except Exception as e:
        sys.stderr.write(f"Erro ao exibir a ajuda!\nErro: {e}\n")


def obter_vertices(vertices):
    """
    Obtém e processa as coordenadas de vértices de um formato específico.

    Esta função recebe uma sequência de coordenadas de vértices no formato "(a,b),(c,d),(e,f)" e a converte em uma lista de
    vértices, onde cada vértice é uma tupla (a, b).

    :param vertices: Sequência de coordenadas de vértices no formato "(a,b),(c,d),(e,f)".
    :type vertices: str
    :return: Uma lista de vértices no formato [(a, b), (c, d), (e, f), ...].
    :rtype: list
    :raises ValueError: Se o formato das coordenadas for inválido.
    """
    try:
        # Remove os parênteses e divide os pontos
        pontos = vertices.split('),(')
        # Limpa os parênteses e divide os valores x e y usando obter_componentes
        lista_vertices = [obter_ponto(ponto) for ponto in pontos]
        if len(lista_vertices) >= 3:
            return lista_vertices
        else:
            tk.messagebox.showerror("Vértices Inválidos!", "Um polígono deve ter no mínimo 3 vértices.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Vértices Inválidos!", "Formato inválido. Use (a,b),(c, d),(e,f)...")
        sys.exit()


def obter_num_pontos(num_pontos):
    """
    Obtém e valida o número de pontos para rasterização.

    Esta função recebe um valor representando o número de pontos para rasterização e valida se é um número inteiro positivo.

    :param num_pontos: O número de pontos para rasterização.
    :type num_pontos: str
    :return: O número de pontos validado como um inteiro positivo.
    :rtype: int
    :raises ValueError: Se o valor não puder ser convertido em um inteiro positivo.
    """
    try:
        num_pontos = int(num_pontos)
        if num_pontos > 0:
            return num_pontos  # Retorna num_pontos
        else:
            messagebox.showerror("Nº de pontos inválido!", "Nº de pontos deve ser positivo.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Nº de pontos inválido!", "Nº de pontos deve ser um inteiro positivo.")
        sys.exit()


def obter_ponto(ponto):
    """
    Obtém e valida as coordenadas de um ponto no plano.

    Esta função recebe uma sequência de coordenadas de ponto no formato "(px, py)" e a converte em um ponto com coordenadas
    (px, py). Além disso, ela verifica se as coordenadas do ponto estão no intervalo de -1 a 1.

    :param ponto: Sequência de coordenadas de ponto no formato "(px, py)".
    :type ponto: str
    :return: Um ponto com coordenadas (px, py) no intervalo de -1 a 1.
    :rtype: tuple
    :raises ValueError: Se o formato das coordenadas for inválido ou se as coordenadas não estiverem no intervalo correto.
    """
    try:
        # Remove os parênteses e divide os valores
        px, py = map(float, ponto.strip('()').split(','))

        # Verifique se x e y estão no intervalo -1 a 1
        if -1 <= px <= 1 and -1 <= py <= 1:
            return px, py
        else:
            messagebox.showerror("Ponto(s) Inválido(s)!", "Valores de Px e Py devem estar no intervalo de -1 a 1.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Ponto(s) e/ou Tangente(s) Inválido(s)!", "Formato inválido. Use (Px, Py)")
        sys.exit()


def obter_tangente(tangente):
    """
    Obtém e valida as coordenadas de um vetor de tangente.

    Esta função recebe uma sequência de coordenadas de vetor de tangente no formato "(tx, ty)" e a converte em um vetor de
    tangente com coordenadas (tx, ty).

    :param tangente: Sequência de coordenadas de vetor de tangente no formato "(tx, ty)".
    :type tangente: str
    :return: Um vetor de tangente com coordenadas (tx, ty).
    :rtype: tuple
    :raises ValueError: Se o formato das coordenadas for inválido.
    """
    try:
        # Remove os parênteses e divide os valores
        tx, ty = map(float, tangente.strip('()').split(','))
        return tx, ty
    except ValueError:
        tk.messagebox.showerror("Tangente(s) Inválida(s)!", "Formato inválido. Use (Tx, Ty)")
        sys.exit()


def obter_resolucao(resolucao):
    """
    Obtém e valida os valores de largura e altura de uma resolução.

    Esta função recebe uma sequência de coordenadas de resolução no formato "(largura, altura)" e a converte em um par de
    valores de largura e altura. Além disso, ela verifica se ambos os valores são números inteiros maiores que zero.

    :param resolucao: Sequência de coordenadas de resolução no formato "(largura, altura)".
    :type resolucao: str
    :return: Um par de valores de largura e altura validados como números inteiros maiores que zero.
    :rtype: tuple
    :raises ValueError: Se o formato das coordenadas for inválido ou se largura e altura não forem números inteiros
    maiores que zero.
    """
    try:
        # Remove os parênteses e divide os valores
        largura, altura = map(int, resolucao.strip('()').split(','))

        # Verifique se largura e altura são inteiros e maiores que zero
        if isinstance(largura, int) and isinstance(altura, int) and largura > 0 and altura > 0:
            return largura, altura
        else:
            messagebox.showerror("Resolução Inválida!", "Largura e altura devem ser números inteiros maiores que zero.")
            sys.exit()
    except ValueError:
        tk.messagebox.showerror("Resolução Inválida!", "Formato inválido. Use (largura, altura)")
        sys.exit()


def obter_cor(rgb):
    """
    Obtém e valida os valores das componentes de cor RGB.

    Esta função recebe uma sequência de coordenadas de cor no formato "(r, g, b)" e a converte em uma tupla com os valores
    das componentes de cor RGB (r, g, b). Além disso, ela verifica se as componentes são números inteiros e estão no
    intervalo de 0 a 255.

    :param rgb: Sequência de coordenadas de cor no formato "(r, g, b)".
    :type rgb: str
    :return: Uma tupla com os valores das componentes de cor RGB (r, g, b).
    :rtype: tuple
    :raises ValueError: Se o formato das coordenadas for inválido, se as componentes não forem números inteiros ou se
    estiverem fora do intervalo de 0 a 255.
    """
    try:
        # Remove os parênteses e divide os valores
        r, g, b = map(int, rgb.strip('()').split(','))

        # Verifique se r, g e b são inteiros
        if isinstance(r, int) and isinstance(g, int) and isinstance(b, int):
            # Verifique se r, g e b estão no intervalo de 0 a 255
            if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
                return r, g, b  # Retorna uma tupla com os valores r, g e b
            else:
                messagebox.showerror("Cor Inválida!", "Valores de r, g e b devem estar no intervalo de 0 a 255.")
                sys.exit()
        else:
            messagebox.showerror("Cor Inválida!", "r, g e b devem ser números inteiros.")
            sys.exit()
    except ValueError:
        messagebox.showerror("Cor Inválida!", "Formato inválido. Use (r, g, b)")
        sys.exit()


def reta():
    """
    Cria uma reta em um aplicativo gráfico.

    Esta função obtém os valores dos pontos inicial e final da reta, a resolução da imagem e a cor da reta a partir de campos
    de entrada. Em seguida, ela chama a função `cg.reta` para desenhar a reta com os parâmetros fornecidos.

    :raises ValueError: Se os valores dos campos de entrada forem inválidos ou se ocorrer um erro ao criar a reta.
    """
    try:
        # Obtenha os valores dos campos p1x, p1y, p2x, p2y, r, g, b, largura, altura e chame a função reta
        p1x, p1y = obter_ponto(p1_entry.get())
        p2x, p2y = obter_ponto(p2_entry.get())
        largura, altura = obter_resolucao(resolucao_entry.get())
        cor = obter_cor(rgb_entry.get())
        cg.reta(p1x, p1y, p2x, p2y, largura, altura, cor)
        print("Reta criada com sucesso!")
    except:
        sys.stderr.write(f"Reta inválida!, verifique os valores!\n")


def plot_resolucao():
    """
    Plota e exibe uma imagem com a resolução especificada em uma nova janela.

    Esta função obtém a largura e a altura da resolução da imagem a partir de um campo de entrada e, em seguida, chama a
    função `cg.plot_resolucao` para exibir a imagem com a resolução especificada.

    :raises ValueError: Se o valor do campo de entrada for inválido ou se ocorrer um erro ao plotar a imagem.
    """
    try:
        largura, altura = obter_resolucao(resolucao_entry.get())
        # Exibe a figura na nova janela
        cg.plot_resolucao(largura, altura)
        print("Imagem plotada com sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagem!\n")


def plot_resolucao_normalizada():
    """
    Plota e exibe uma imagem com a resolução especificada, mas com coordenadas normalizadas (-1 a 1) em uma nova janela.

    Esta função obtém a largura e a altura da resolução da imagem a partir de um campo de entrada e, em seguida, chama a
    função `cg.plot_resolucao_normalizada` para exibir a imagem com as coordenadas normalizadas.

    :raises ValueError: Se o valor do campo de entrada for inválido ou se ocorrer um erro ao plotar a imagem normalizada.
    """
    try:
        largura, altura = obter_resolucao(resolucao_entry.get())
        # Exibe a figura na nova janela
        cg.plot_resolucao_normalizada(largura, altura)
        print("Imagem normalizada plotada com Sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagem normalizada!\n")


def plot_tudo():
    """
    Plota e exibe todas as imagens disponíveis na interface gráfica em uma única figura.

    Esta função chama a função `cg.plot_tudo` para exibir todas as imagens plotadas na interface em uma única figura.

    :raises ValueError: Se ocorrer um erro ao plotar as imagens.
    """
    try:
        cg.plot_tudo()
        print("Imagens plotadas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar imagens!\n")


def plot_normalizado():
    """
    Plota e exibe todas as imagens disponíveis na interface gráfica com coordenadas normalizadas (-1 a 1)
    em uma única figura.

    Esta função chama a função `cg.plot_tudo_normalizado` para exibir todas as imagens plotadas na interface
    com coordenadas normalizadas em uma única figura.

    :raises ValueError: Se ocorrer um erro ao plotar as imagens normalizadas.
    """
    try:
        cg.plot_tudo_normalizado()
        print("Imagens normalizadas plotadas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao plotar Imagens normalizadas!\n")


def curva():
    """
    Cria e adiciona uma curva de Hermite na interface gráfica.

    Esta função obtém os valores dos campos, como as coordenadas dos pontos inicial e final, vetores tangentes, número de pontos,
    cor, largura e altura da imagem, e chama a função `cg.curva_hermite` para desenhar a curva de Hermite.

    :raises ValueError: Se ocorrer um erro ao criar ou adicionar a curva de Hermite.
    """
    try:
        # Obtenha os valores dos campos p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, r, g, b, l,
        # e chame a função rasterizar_curva_hermite
        p1x, p1y = obter_ponto(p1_entry.get())
        p2x, p2y = obter_ponto(p2_entry.get())
        t1x, t1y = obter_tangente(t1_entry.get())
        t2x, t2y = obter_tangente(t2_entry.get())
        num_pontos = obter_num_pontos(num_pontos_entry.get())
        cor = obter_cor(rgb_entry.get())
        largura, altura = obter_resolucao(resolucao_entry.get())
        cg.curva_hermite(p1x, p1y, p2x, p2y, t1x, t1y, t2x, t2y, num_pontos, largura, altura, cor)
        print("Curva adicionada com sucesso!")
    except:
        sys.stderr.write(f"Curva inválida!, verifique os valores!\n")


def poligono():
    """
    Cria e adiciona um polígono na interface gráfica.

    Esta função obtém os valores do campo de vértices do polígono, cor, largura e altura da imagem
    e chama a função `cg.poligono` para desenhar o polígono.

    :raises ValueError: Se ocorrer um erro ao criar ou adicionar o polígono.
    """
    try:
        # Obtenha os valores dos campos vertices, r, g, b, l, e chame a função poligono
        vertices = obter_vertices(vertices_entry.get())
        cor = obter_cor(rgb_entry.get())
        largura, altura = obter_resolucao(resolucao_entry.get())
        cg.poligono(vertices, largura, altura, cor)
        print("Polígono criado com sucesso!")
    except:
        sys.stderr.write(f"Polígono inválido! Verifique os valores!\n")


def deleta_resolucao():
    """
    Exclui uma resolução da interface gráfica.

    Esta função obtém os valores de largura e altura da imagem a ser excluída
    e chama a função `cg.deleta_resolucao` para realizar a exclusão.

    :raises ValueError: Se ocorrer um erro ao excluir a resolução.
    """
    try:
        largura, altura = obter_resolucao(resolucao_entry.get())
        cg.deleta_resolucao(largura, altura)
        print("Resolução excluída com sucesso!")
    except:
        sys.stderr.write(f"Erro ao deletar resolução!\n")


def deleta_tudo():
    """
    Exclui todas as resoluções da interface gráfica.

    Esta função chama a função `cg.deleta_tudo` para excluir todas as resoluções
    que foram plotadas na interface.

    :raises ValueError: Se ocorrer um erro ao excluir as resoluções.
    """
    try:
        cg.deleta_tudo()
        print("Resoluções excluídas com sucesso!")
    except:
        sys.stderr.write(f"Erro ao deletar todas as resoluções!\n")


# Crie uma janela principal
janela = tk.Tk()
janela.title("Computação Gráfica")
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

plotar_button = tk.Button(janela, text="Plotar Todas Resoluções", command=plot_tudo)
plotar_button.grid(row=0, column=5, columnspan=1, sticky="nsew")

plotar_button = tk.Button(janela, text="Plotar Todas Resoluções Normalizado", command=plot_normalizado)
plotar_button.grid(row=1, column=5, columnspan=1, sticky="nsew")

# Criar um botão exemplo
botao_exemplo = tk.Button(janela, text="Exemplos", command=exemplos)
botao_exemplo.grid(row=3, column=4, sticky="nsew")

# Criar um botão de ajuda
botao_ajuda = tk.Button(janela, text="Ajuda", command=exibir_ajuda)
botao_ajuda.grid(row=3, column=5, sticky="nsew")

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
