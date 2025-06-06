import tkinter as tk
from tkinter import ttk

class AbaVisualizacao(tk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema

        # Campo de busca
        self.entry_busca = tk.Entry(self)
        self.entry_busca.pack(pady=5, side="left")
        self.btn_buscar = tk.Button(self, text="Buscar", command=self.simular_busca)
        self.btn_buscar.pack(pady=5, side="left")

        # Botão "Carregar"
        self.btn_carregar = tk.Button(self, text="Carregar", command=self.atualizar_visualizacao)
        self.btn_carregar.pack(pady=5, side="left")

        self.canvas = tk.Canvas(self, bg="white", width=950, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.atualizar_visualizacao()

    def atualizar_visualizacao(self, caminho=None):
        self.canvas.delete("all")
        raiz = self.sistema.arvore_livros_por_titulo.raiz
        if raiz:
            self._desenhar_no(raiz, 475, 20, 220, caminho or [])
        else:
            self.canvas.create_text(475, 300, text="Nenhum livro cadastrado.", font=("Arial", 16), fill="gray")

    def _desenhar_no(self, no, x, y, dx, caminho):
        cor = "lightblue"
        if no in caminho:
            cor = "yellow"
        self.canvas.create_oval(x - 30, y - 20, x + 30, y + 20, fill=cor, outline="black")
        self.canvas.create_text(x, y, text=no.livro.titulo[:15], font=("Arial", 10))

        min_dx = 40  # espaçamento mínimo horizontal
        next_dx = max(dx // 1.7, min_dx)
        y_step = 80  # espaçamento vertical

        if no.esquerda:
            self.canvas.create_line(x, y + 20, x - next_dx, y + y_step - 20, fill="black")
            self._desenhar_no(no.esquerda, x - next_dx, y + y_step, next_dx, caminho)
        if no.direita:
            self.canvas.create_line(x, y + 20, x + next_dx, y + y_step - 20, fill="black")
            self._desenhar_no(no.direita, x + next_dx, y + y_step, next_dx, caminho)

    def simular_busca(self):
        titulo = self.entry_busca.get().strip().lower()
        caminho = []
        no = self.sistema.arvore_livros_por_titulo.raiz
        while no:
            caminho.append(no)
            if titulo == no.chave:
                break
            elif titulo < no.chave:
                no = no.esquerda
            else:
                no = no.direita
        self.atualizar_visualizacao(caminho)