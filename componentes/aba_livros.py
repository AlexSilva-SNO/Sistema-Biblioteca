import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

class AbaLivros(tb.Frame):
    def __init__(self, master, sistema, usuario_logado, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sistema = sistema
        self.usuario_logado = usuario_logado
        self.configure(padding=18)

        # Título
        tb.Label(self, text="📚 Livros", font=("Segoe UI", 19, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 16))

        # ---- SCROLLABLE CARDS ----
        self.cards_canvas = tk.Canvas(self, bg="#232629", highlightthickness=0, borderwidth=0, relief="flat")
        self.cards_frame = tb.Frame(self.cards_canvas)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.cards_canvas.yview)
        self.cards_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.cards_canvas.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="y", side="right")

        self.cards_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.cards_frame.bind("<Configure>", lambda e: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all")))

        tb.Separator(self, orient="horizontal").pack(fill="x", pady=14)

        # Botões principais
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=7)
        tb.Button(btn_frame, text="Atualizar", bootstyle="secondary-outline", width=12, command=self.mostrar_cards_livros).pack(side="left", padx=4)
        if usuario_logado.tipo == "Funcionario":
            tb.Button(btn_frame, text="Novo", bootstyle="success-outline", width=12, command=self.mostrar_form_livro).pack(side="left", padx=4)

        # Formulário de cadastro/edição de livros
        self.frame_form_livro = tb.Frame(self, padding=10)
        tb.Label(self.frame_form_livro, text="Cadastro/Edição de Livro", font=("Segoe UI", 15, "bold"), bootstyle="inverse-dark").pack(pady=(0, 7))

        form = tb.Frame(self.frame_form_livro)
        form.pack(pady=5)
        labels = ["Título:", "Autor:", "ISBN:", "Quantidade:"]  # Mantém ISBN para o usuário digitar
        self.entries = []
        for i, label in enumerate(labels):
            tb.Label(form, text=label, font=("Segoe UI", 11)).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tb.Entry(form, width=37, font=("Segoe UI", 11))
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries.append(entry)
        self.titulo_var, self.autor_var, self.isbn_var, self.qtd_var = self.entries

        btns = tb.Frame(self.frame_form_livro)
        btns.pack(pady=(14, 0))
        tb.Button(btns, text="Salvar", bootstyle="success", width=12, command=self.salvar_livro).pack(side="left", padx=6)
        tb.Button(btns, text="Cancelar", bootstyle="secondary", width=12, command=self.mostrar_cards_livros).pack(side="left", padx=6)

        self.mostrar_cards_livros()
        self.editando_livro_isbn = None

    def mostrar_form_livro(self):
        self.cards_canvas.pack_forget()
        self.scrollbar.pack_forget()
        self.frame_form_livro.pack(fill="x", pady=24)

    def mostrar_cards_livros(self):
        self.frame_form_livro.pack_forget()
        self.cards_canvas.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="y", side="right")
        self.editando_livro_isbn = None
        self._atualizar_cards_livros()

    def _atualizar_cards_livros(self):
        # Limpa cards antigos
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        livros = self.sistema.arvore_livros_por_titulo.listar_todos_em_ordem()
        if not livros:
            tb.Label(self.cards_frame, text="Nenhum livro cadastrado.", font=("Segoe UI", 13), bootstyle="secondary").pack(pady=30)
            return

        for livro in livros:
            card = tb.Frame(
                self.cards_frame, 
                bootstyle="dark", 
                padding=16, 
                relief="raised", 
                borderwidth=2
            )
            card.pack(fill="x", expand=True, pady=10, padx=8)

            # Título em destaque
            tb.Label(card, text=livro.titulo, font=("Segoe UI", 14, "bold"), bootstyle="inverse-dark").pack(anchor="w")
            tb.Label(card, text=f"Autor: {livro.autor}", font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 0))
            tb.Label(card, text=f"ID: {livro.id_livro}", font=("Segoe UI", 11)).pack(anchor="w")  # Exibe ID do livro
            tb.Label(card, text=f"ISBN: {livro.isbn}", font=("Segoe UI", 11)).pack(anchor="w")  # Exibe ISBN do livro
            tb.Label(card, text=f"Exemplares: {livro.quantidade_exemplares}", font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 2))

            # Botões de ação (só para funcionários)
            if self.usuario_logado.tipo == "Funcionario":
                btns = tb.Frame(card, bootstyle="dark")
                btns.pack(anchor="e", pady=(4,0))
                tb.Button(btns, text="Editar", bootstyle="warning-outline", width=8,
                          command=lambda l=livro: self.abrir_edicao_livro(l)).pack(side="left", padx=3)
                tb.Button(btns, text="Excluir", bootstyle="danger-outline", width=8,
                          command=lambda l=livro: self.confirmar_exclusao_livro(l)).pack(side="left", padx=3)

    def salvar_livro(self):
        titulo = self.titulo_var.get()
        autor = self.autor_var.get()
        isbn = self.isbn_var.get()
        try:
            quantidade = int(self.qtd_var.get())
        except ValueError:
            Messagebox.show_error("Quantidade inválida!", "Erro")
            return
        if not titulo or not autor or not isbn or quantidade < 0:
            Messagebox.show_error("Preencha todos os campos corretamente!", "Erro")
            return

        # Edição
        if self.editando_livro_isbn:
            livro = self.sistema.mapa_isbn_livro.get(self.editando_livro_isbn)
            if not livro:
                Messagebox.show_error("Livro não encontrado!", "Erro")
                return
            livro.titulo = titulo
            livro.autor = autor
            livro.isbn = isbn
            livro.quantidade_exemplares = quantidade
            if isbn != self.editando_livro_isbn:
                self.sistema.mapa_isbn_livro.pop(self.editando_livro_isbn)
                self.sistema.mapa_isbn_livro[isbn] = livro
            Messagebox.show_info("Livro editado com sucesso!", "Sucesso")
        else:
            # Cadastro
            sucesso = self.sistema.cadastrar_livro(titulo, autor, isbn, quantidade)
            if sucesso:
                Messagebox.show_info("Livro cadastrado com sucesso!", "Sucesso")
            else:
                Messagebox.show_error("Livro com este ISBN já cadastrado!", "Erro")
        self.sistema.salvar_dados()
        self.titulo_var.delete(0, tk.END)
        self.autor_var.delete(0, tk.END)
        self.isbn_var.delete(0, tk.END)
        self.qtd_var.delete(0, tk.END)
        self.mostrar_cards_livros()

    def abrir_edicao_livro(self, livro):
        self.titulo_var.delete(0, tk.END)
        self.autor_var.delete(0, tk.END)
        self.isbn_var.delete(0, tk.END)
        self.qtd_var.delete(0, tk.END)
        self.titulo_var.insert(0, livro.titulo)
        self.autor_var.insert(0, livro.autor)
        self.isbn_var.insert(0, livro.isbn)
        self.qtd_var.insert(0, str(livro.quantidade_exemplares))
        self.editando_livro_isbn = livro.isbn
        self.mostrar_form_livro()

    def confirmar_exclusao_livro(self, livro):
        if Messagebox.okcancel(f"Tem certeza que deseja excluir o livro '{livro.titulo}' (ISBN {livro.isbn})?", "Confirmar exclusão"):
            if livro.isbn in self.sistema.mapa_isbn_livro:
                self.sistema.mapa_isbn_livro.pop(livro.isbn)
            self.sistema.arvore_livros_por_titulo.remover(livro.isbn)
            self.sistema.salvar_dados()
            self.mostrar_cards_livros()
            Messagebox.show_info("Livro excluído com sucesso.", "Sucesso")
