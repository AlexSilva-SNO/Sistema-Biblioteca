import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

from sistema_biblioteca import SistemaBiblioteca
from componentes.Login import TelaLogin
from componentes.aba_livros import AbaLivros
from componentes.aba_usuarios import AbaUsuarios
from componentes.aba_emprestimos import AbaEmprestimos
from componentes.aba_historico import AbaHistorico

class BibliotecaApp:
    def __init__(self, root):
        self.sistema = SistemaBiblioteca(arquivo_dados="minha_biblioteca.json")
        self.root = root
        self.usuario_logado = None

        # Tela de login inicial (abre antes do resto)
        self.tela_login = TelaLogin(self.root, self.entrar_no_sistema)
        self.root.withdraw()

    def entrar_no_sistema(self, matricula, senha, login_window):
        usuario = self.sistema.autenticar_usuario(matricula, senha)
        if usuario:
            self.usuario_logado = usuario
            login_window.destroy()
            self.mostrar_janela_principal()
        else:
            Messagebox.show_error("Matrícula ou senha incorretos!", "Erro")

    def mostrar_janela_principal(self):
        self.root.deiconify()
        self.root.title(f"Sistema de Biblioteca - {self.usuario_logado.nome} ({self.usuario_logado.tipo})")
        self.root.geometry("1000x650")
        self.root.resizable(False, False)

        style = tb.Style("darkly")  # Tema escuro e elegante
        self.notebook = tb.Notebook(self.root, bootstyle="dark")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Aba Livros (disponível para todos)
        self.aba_livros = AbaLivros(self.notebook, self.sistema, self.usuario_logado)
        self.notebook.add(self.aba_livros, text="Livros")

        # Aba Usuários (apenas para Funcionário)
        if self.usuario_logado and self.usuario_logado.tipo == "Funcionario":
            self.aba_usuarios = AbaUsuarios(self.notebook, self.sistema)
            self.notebook.add(self.aba_usuarios, text="Usuários")

        # Aba Empréstimos (todos visualizam)
        self.aba_emprestimos = AbaEmprestimos(self.notebook, self.sistema, self.usuario_logado)
        self.notebook.add(self.aba_emprestimos, text="Empréstimos")

        # Aba Histórico (todos visualizam)
        self.aba_historico = AbaHistorico(self.notebook, self.sistema, self.usuario_logado)
        self.notebook.add(self.aba_historico, text="Histórico")

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def fechar_janela(self):
        self.sistema.salvar_dados()
        self.root.destroy()

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = BibliotecaApp(root)
    root.mainloop()