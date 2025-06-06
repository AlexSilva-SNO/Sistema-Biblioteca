import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox  # Adicione este import
from sistema_biblioteca import SistemaBiblioteca

class BibliotecaApp:
    def __init__(self, root):
        self.sistema = SistemaBiblioteca(arquivo_dados="minha_biblioteca.json")
        self.root = root
        self.root.title("Sistema de Biblioteca")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Tema bonito
        style = tb.Style("superhero")

        # Notebook (abas)
        self.notebook = tb.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Abas
        self.frame_livros = tb.Frame(self.notebook)
        self.frame_usuarios = tb.Frame(self.notebook)
        self.frame_emprestimos = tb.Frame(self.notebook)
        self.frame_historico = tb.Frame(self.notebook)

        self.notebook.add(self.frame_livros, text="Livros")
        self.notebook.add(self.frame_usuarios, text="Usuários")
        self.notebook.add(self.frame_emprestimos, text="Empréstimos")
        self.notebook.add(self.frame_historico, text="Histórico")

        self.criar_aba_livros()
        self.criar_aba_usuarios()

    def criar_aba_livros(self):
        frame = self.frame_livros

        # Frame para listagem
        self.frame_lista_livros = tb.Frame(frame)
        self.frame_lista_livros.pack(fill="both", expand=True)

        tb.Label(self.frame_lista_livros, text="Livros Cadastrados", font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.livros_listbox = tk.Listbox(self.frame_lista_livros, width=80, height=15)
        self.livros_listbox.pack(pady=10)
        tb.Button(self.frame_lista_livros, text="Atualizar Lista", bootstyle="info", command=self.atualizar_lista_livros).pack(pady=5)
        tb.Button(self.frame_lista_livros, text="Novo Livro", bootstyle="success", command=self.mostrar_form_livro).pack(pady=5)

        # Frame para cadastro
        self.frame_form_livro = tb.Frame(frame)

        tb.Label(self.frame_form_livro, text="Cadastro de Livro", font=("Segoe UI", 16, "bold")).pack(pady=10)
        form = tb.Frame(self.frame_form_livro)
        form.pack(pady=10)

        tb.Label(form, text="Título:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Autor:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="ISBN:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Quantidade:").grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.titulo_var = tk.StringVar()
        self.autor_var = tk.StringVar()
        self.isbn_var = tk.StringVar()
        self.qtd_var = tk.StringVar()

        tb.Entry(form, textvariable=self.titulo_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.autor_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.isbn_var, width=40).grid(row=2, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.qtd_var, width=10).grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tb.Button(form, text="Salvar Livro", bootstyle="success", command=self.salvar_livro).grid(row=4, column=0, columnspan=2, pady=10)
        tb.Button(self.frame_form_livro, text="Voltar para Lista", bootstyle="secondary", command=self.mostrar_lista_livros).pack(pady=5)

        self.mostrar_lista_livros()  # Mostra a lista ao iniciar

    def mostrar_form_livro(self):
        self.frame_lista_livros.pack_forget()
        self.frame_form_livro.pack(fill="both", expand=True)

    def mostrar_lista_livros(self):
        self.frame_form_livro.pack_forget()
        self.frame_lista_livros.pack(fill="both", expand=True)
        self.atualizar_lista_livros()

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

        sucesso = self.sistema.cadastrar_livro(titulo, autor, isbn, quantidade)
        # Limpa os campos ANTES de atualizar a lista
        self.titulo_var.set("")
        self.autor_var.set("")
        self.isbn_var.set("")
        self.qtd_var.set("")
        if sucesso:
            self.sistema.salvar_dados()  # Salva imediatamente após cadastrar
            Messagebox.show_info("Livro cadastrado com sucesso!", "Sucesso")
        else:
            Messagebox.show_error("Livro com este ISBN já cadastrado!", "Erro")
        self.atualizar_lista_livros()

    def atualizar_lista_livros(self):
        self.livros_listbox.delete(0, tk.END)
        livros = self.sistema.arvore_livros_por_titulo.listar_todos_em_ordem()
        for livro in livros:
            self.livros_listbox.insert(
                tk.END,
                f"{livro.titulo} | {livro.autor} | {livro.isbn} | {livro.quantidade_exemplares} exemplares"
            )

    def criar_aba_usuarios(self):
        frame = self.frame_usuarios

        # Frame para listagem
        self.frame_lista_usuarios = tb.Frame(frame)
        self.frame_lista_usuarios.pack(fill="both", expand=True)

        tb.Label(self.frame_lista_usuarios, text="Usuários Cadastrados", font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.usuarios_listbox = tk.Listbox(self.frame_lista_usuarios, width=80, height=15)
        self.usuarios_listbox.pack(pady=10)
        tb.Button(self.frame_lista_usuarios, text="Atualizar Lista", bootstyle="info", command=self.atualizar_lista_usuarios).pack(pady=5)
        tb.Button(self.frame_lista_usuarios, text="Novo Usuário", bootstyle="success", command=self.mostrar_form_usuario).pack(pady=5)

        # Frame para cadastro
        self.frame_form_usuario = tb.Frame(frame)

        tb.Label(self.frame_form_usuario, text="Cadastro de Usuário", font=("Segoe UI", 16, "bold")).pack(pady=10)
        form = tb.Frame(self.frame_form_usuario)
        form.pack(pady=10)

        tb.Label(form, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Matrícula:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Curso:").grid(row=2, column=0, sticky="e", padx=5, pady=5)

        self.nome_var = tk.StringVar()
        self.matricula_var = tk.StringVar()
        self.curso_var = tk.StringVar()

        tb.Entry(form, textvariable=self.nome_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.matricula_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.curso_var, width=40).grid(row=2, column=1, padx=5, pady=5)

        tb.Button(form, text="Salvar Usuário", bootstyle="success", command=self.salvar_usuario).grid(row=3, column=0, columnspan=2, pady=10)
        tb.Button(self.frame_form_usuario, text="Voltar para Lista", bootstyle="secondary", command=self.mostrar_lista_usuarios).pack(pady=5)

        self.mostrar_lista_usuarios()  # Mostra a lista ao iniciar

    def mostrar_form_usuario(self):
        self.frame_lista_usuarios.pack_forget()
        self.frame_form_usuario.pack(fill="both", expand=True)

    def mostrar_lista_usuarios(self):
        self.frame_form_usuario.pack_forget()
        self.frame_lista_usuarios.pack(fill="both", expand=True)
        self.atualizar_lista_usuarios()

    def salvar_usuario(self):
        nome = self.nome_var.get()
        matricula = self.matricula_var.get()
        curso = self.curso_var.get()

        if not nome or not matricula or not curso:
            tb.Messagebox.show_error("Preencha todos os campos!", "Erro")
            return

        sucesso = self.sistema.cadastrar_usuario(nome, matricula, curso)
        if sucesso:
            tb.Messagebox.show_info("Usuário cadastrado com sucesso!", "Sucesso")
        else:
            tb.Messagebox.show_error("Usuário com esta matrícula já cadastrado!", "Erro")
        self.atualizar_lista_usuarios()
        self.nome_var.set("")
        self.matricula_var.set("")
        self.curso_var.set("")

    def atualizar_lista_usuarios(self):
        self.usuarios_listbox.delete(0, tk.END)
        usuarios = self.sistema.lista_usuarios.listar_todos()
        for usuario in usuarios:
            self.usuarios_listbox.insert(
                tk.END,
                f"{usuario.nome} | {usuario.matricula} | {usuario.curso}"
            )

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = BibliotecaApp(root)
    root.mainloop()