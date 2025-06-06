import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox
from sistema_biblioteca import SistemaBiblioteca

class TelaLogin:
    def __init__(self, master, on_login):
        self.top = tk.Toplevel(master)
        self.top.title("Login - Biblioteca")
        self.top.geometry("320x220")
        self.top.resizable(False, False)
        self.top.grab_set()
        self.on_login = on_login

        tb.Label(self.top, text="Matrícula:", font=("Segoe UI", 12)).pack(pady=(16, 0))
        self.matricula_var = tk.StringVar()
        tb.Entry(self.top, textvariable=self.matricula_var, width=30).pack()

        tb.Label(self.top, text="Senha:", font=("Segoe UI", 12)).pack(pady=(8, 0))
        self.senha_var = tk.StringVar()
        tb.Entry(self.top, textvariable=self.senha_var, width=30, show="*").pack()

        tb.Button(self.top, text="Entrar", bootstyle="success", command=self.login).pack(pady=16)

    def login(self):
        matricula = self.matricula_var.get()
        senha = self.senha_var.get()
        if not matricula or not senha:
            Messagebox.show_error("Preencha todos os campos!", "Erro")
            return
        self.on_login(matricula, senha, self.top)

class BibliotecaApp:
    def __init__(self, root):
        self.sistema = SistemaBiblioteca(arquivo_dados="minha_biblioteca.json")
        self.root = root
        self.usuario_logado = None
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
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        style = tb.Style("superhero")
        self.notebook = tb.Notebook(self.root, bootstyle="primary")
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.frame_livros = tb.Frame(self.notebook)
        self.frame_usuarios = tb.Frame(self.notebook)
        self.frame_emprestimos = tb.Frame(self.notebook)
        self.frame_historico = tb.Frame(self.notebook)

        self.notebook.add(self.frame_livros, text="Livros")
        if self.usuario_logado and self.usuario_logado.tipo == "Funcionario":
            self.notebook.add(self.frame_usuarios, text="Usuários")
            self.criar_aba_usuarios()

        self.notebook.add(self.frame_emprestimos, text="Empréstimos")
        self.notebook.add(self.frame_historico, text="Histórico")

        self.criar_aba_livros()
        self.criar_aba_emprestimos()
        self.criar_aba_historico()

        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def fechar_janela(self):
        self.sistema.salvar_dados()
        self.root.destroy()

    # ==== LIVROS ====
    def criar_aba_livros(self):
        frame = self.frame_livros
        self.frame_lista_livros = tb.Frame(frame)
        self.frame_lista_livros.pack(fill="both", expand=True)
        tb.Label(self.frame_lista_livros, text="Livros Cadastrados", font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.livros_listbox = tk.Listbox(self.frame_lista_livros, width=80, height=15)
        self.livros_listbox.pack(pady=10)
        tb.Button(self.frame_lista_livros, text="Atualizar Lista", bootstyle="info", command=self.atualizar_lista_livros).pack(pady=5)
        
        # Botões só para funcionários
        if self.usuario_logado and self.usuario_logado.tipo == "Funcionario":
            tb.Button(self.frame_lista_livros, text="Novo Livro", bootstyle="success", command=self.mostrar_form_livro).pack(pady=5)
            tb.Button(self.frame_lista_livros, text="Editar Livro Selecionado", bootstyle="warning", command=self.editar_livro_selecionado).pack(pady=5)
            tb.Button(self.frame_lista_livros, text="Excluir Livro Selecionado", bootstyle="danger", command=self.excluir_livro_selecionado).pack(pady=5)

        self.frame_form_livro = tb.Frame(frame)
        tb.Label(self.frame_form_livro, text="Cadastro/Edição de Livro", font=("Segoe UI", 16, "bold")).pack(pady=10)
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
        self.btn_salvar_livro = tb.Button(form, text="Salvar Livro", bootstyle="success", command=self.salvar_livro)
        self.btn_salvar_livro.grid(row=4, column=0, columnspan=2, pady=10)
        tb.Button(self.frame_form_livro, text="Voltar para Lista", bootstyle="secondary", command=self.mostrar_lista_livros).pack(pady=5)
        self.mostrar_lista_livros()
        self.editando_livro_isbn = None

    def mostrar_form_livro(self):
        self.frame_lista_livros.pack_forget()
        self.frame_form_livro.pack(fill="both", expand=True)

    def mostrar_lista_livros(self):
        self.frame_form_livro.pack_forget()
        self.frame_lista_livros.pack(fill="both", expand=True)
        self.atualizar_lista_livros()
        self.editando_livro_isbn = None

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
            sucesso = self.sistema.cadastrar_livro(titulo, autor, isbn, quantidade)
            if sucesso:
                Messagebox.show_info("Livro cadastrado com sucesso!", "Sucesso")
            else:
                Messagebox.show_error("Livro com este ISBN já cadastrado!", "Erro")
        self.sistema.salvar_dados()
        self.titulo_var.set("")
        self.autor_var.set("")
        self.isbn_var.set("")
        self.qtd_var.set("")
        self.atualizar_lista_livros()
        self.mostrar_lista_livros()

    def atualizar_lista_livros(self):
        self.livros_listbox.delete(0, tk.END)
        livros = self.sistema.arvore_livros_por_titulo.listar_todos_em_ordem()
        for livro in livros:
            self.livros_listbox.insert(
                tk.END,
                f"{livro.titulo} | {livro.autor} | {livro.isbn} | {livro.quantidade_exemplares} exemplares"
            )

    def editar_livro_selecionado(self):
        selecionado = self.livros_listbox.curselection()
        if not selecionado:
            Messagebox.show_error("Selecione um livro para editar.", "Erro")
            return
        livro_str = self.livros_listbox.get(selecionado[0])
        isbn = livro_str.split('|')[2].strip()
        livro = self.sistema.mapa_isbn_livro.get(isbn)
        if not livro:
            Messagebox.show_error("Livro não encontrado!", "Erro")
            return
        self.editando_livro_isbn = isbn
        self.titulo_var.set(livro.titulo)
        self.autor_var.set(livro.autor)
        self.isbn_var.set(livro.isbn)
        self.qtd_var.set(str(livro.quantidade_exemplares))
        self.mostrar_form_livro()

    def excluir_livro_selecionado(self):
        selecionado = self.livros_listbox.curselection()
        if not selecionado:
            Messagebox.show_error("Selecione um livro para excluir.", "Erro")
            return
        livro_str = self.livros_listbox.get(selecionado[0])
        isbn = livro_str.split('|')[2].strip()
        if Messagebox.okcancel(f"Tem certeza que deseja excluir o livro com ISBN {isbn}?", "Confirmar exclusão"):
            # Remove do dicionário auxiliar
            if isbn in self.sistema.mapa_isbn_livro:
                self.sistema.mapa_isbn_livro.pop(isbn)
            # Remove da Árvore Binária
            self.sistema.arvore_livros_por_titulo.remover(isbn)
            self.sistema.salvar_dados()
            self.atualizar_lista_livros()
            Messagebox.show_info("Livro excluído com sucesso.", "Sucesso")

    # ==== USUÁRIOS ====
    def criar_aba_usuarios(self):
        frame = self.frame_usuarios
        self.frame_lista_usuarios = tb.Frame(frame)
        self.frame_lista_usuarios.pack(fill="both", expand=True)
        tb.Label(self.frame_lista_usuarios, text="Usuários Cadastrados", font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.usuarios_listbox = tk.Listbox(self.frame_lista_usuarios, width=80, height=15)
        self.usuarios_listbox.pack(pady=10)
        tb.Button(self.frame_lista_usuarios, text="Atualizar Lista", bootstyle="info", command=self.atualizar_lista_usuarios).pack(pady=5)
        tb.Button(self.frame_lista_usuarios, text="Novo Usuário", bootstyle="success", command=self.mostrar_form_usuario).pack(pady=5)
        tb.Button(self.frame_lista_usuarios, text="Editar Usuário Selecionado", bootstyle="warning", command=self.editar_usuario_selecionado).pack(pady=5)
        tb.Button(self.frame_lista_usuarios, text="Excluir Usuário Selecionado", bootstyle="danger", command=self.excluir_usuario_selecionado).pack(pady=5)
        self.frame_form_usuario = tb.Frame(frame)
        self.tipo_var = tk.StringVar(value="Cliente")
        self.senha_var = tk.StringVar()
        tb.Label(self.frame_form_usuario, text="Cadastro/Edição de Usuário", font=("Segoe UI", 16, "bold")).pack(pady=10)
        form = tb.Frame(self.frame_form_usuario)
        form.pack(pady=10)
        tb.Label(form, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Matrícula:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Curso:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Tipo:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        tb.Label(form, text="Senha:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        tb.Combobox(form, textvariable=self.tipo_var, values=["Cliente", "Funcionario"], state="readonly", width=37).grid(row=3, column=1, padx=5, pady=5)
        self.nome_var = tk.StringVar()
        self.matricula_var = tk.StringVar()
        self.curso_var = tk.StringVar()
        tb.Entry(form, textvariable=self.nome_var, width=40).grid(row=0, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.matricula_var, width=40).grid(row=1, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.curso_var, width=40).grid(row=2, column=1, padx=5, pady=5)
        tb.Entry(form, textvariable=self.senha_var, width=40, show="*").grid(row=4, column=1, padx=5, pady=5)
        tb.Button(form, text="Salvar Usuário", bootstyle="success", command=self.salvar_usuario).grid(row=5, column=0, columnspan=2, pady=10)
        tb.Button(self.frame_form_usuario, text="Voltar para Lista", bootstyle="secondary", command=self.mostrar_lista_usuarios).pack(pady=5)
        self.mostrar_lista_usuarios()
        self.editando_usuario_matricula = None

    def mostrar_form_usuario(self):
        self.frame_lista_usuarios.pack_forget()
        self.frame_form_usuario.pack(fill="both", expand=True)

    def mostrar_lista_usuarios(self):
        self.frame_form_usuario.pack_forget()
        self.frame_lista_usuarios.pack(fill="both", expand=True)
        self.atualizar_lista_usuarios()
        self.editando_usuario_matricula = None

    def salvar_usuario(self):
        nome = self.nome_var.get()
        matricula = self.matricula_var.get()
        curso = self.curso_var.get()
        tipo = self.tipo_var.get()
        senha = self.senha_var.get()
        if not nome or not matricula or not curso or tipo not in ["Cliente", "Funcionario"] or not senha:
            Messagebox.show_error("Preencha todos os campos!", "Erro")
            return

        if self.editando_usuario_matricula:
            usuario = self.sistema.mapa_matricula_usuario.get(self.editando_usuario_matricula)
            if not usuario:
                Messagebox.show_error("Usuário não encontrado!", "Erro")
                return
            usuario.nome = nome
            usuario.matricula = matricula
            usuario.curso = curso
            usuario.tipo = tipo
            usuario.senha = senha
            if matricula != self.editando_usuario_matricula:
                self.sistema.mapa_matricula_usuario.pop(self.editando_usuario_matricula)
                self.sistema.mapa_matricula_usuario[matricula] = usuario
            Messagebox.show_info("Usuário editado com sucesso!", "Sucesso")
        else:
            sucesso = self.sistema.cadastrar_usuario(nome, matricula, curso, tipo, senha)
            if sucesso:
                Messagebox.show_info("Usuário cadastrado com sucesso!", "Sucesso")
            else:
                Messagebox.show_error("Usuário com esta matrícula já cadastrado!", "Erro")
        self.sistema.salvar_dados()
        self.nome_var.set("")
        self.matricula_var.set("")
        self.curso_var.set("")
        self.tipo_var.set("Cliente")
        self.senha_var.set("")
        self.atualizar_lista_usuarios()
        self.mostrar_lista_usuarios()

    def atualizar_lista_usuarios(self):
        self.usuarios_listbox.delete(0, tk.END)
        usuarios = self.sistema.lista_usuarios.listar_todos()
        for usuario in usuarios:
            self.usuarios_listbox.insert(
                tk.END,
                f"{usuario.nome} | {usuario.matricula} | {usuario.curso} | {usuario.tipo}"
            )

    def editar_usuario_selecionado(self):
        selecionado = self.usuarios_listbox.curselection()
        if not selecionado:
            Messagebox.show_error("Selecione um usuário para editar.", "Erro")
            return
        usuario_str = self.usuarios_listbox.get(selecionado[0])
        matricula = usuario_str.split('|')[1].strip()
        usuario = self.sistema.mapa_matricula_usuario.get(matricula)
        if not usuario:
            Messagebox.show_error("Usuário não encontrado!", "Erro")
            return
        self.editando_usuario_matricula = matricula
        self.nome_var.set(usuario.nome)
        self.matricula_var.set(usuario.matricula)
        self.curso_var.set(usuario.curso)
        self.tipo_var.set(usuario.tipo)
        self.senha_var.set(usuario.senha)
        self.mostrar_form_usuario()

    def excluir_usuario_selecionado(self):
        selecionado = self.usuarios_listbox.curselection()
        if not selecionado:
            Messagebox.show_error("Selecione um usuário para excluir.", "Erro")
            return
        usuario_str = self.usuarios_listbox.get(selecionado[0])
        matricula = usuario_str.split('|')[1].strip()
        if matricula == "root":
            Messagebox.show_error("Não é permitido excluir o usuário root.", "Erro")
            return
        if Messagebox.okcancel(f"Tem certeza que deseja excluir o usuário de matrícula {matricula}?", "Confirmar exclusão"):
            if matricula in self.sistema.mapa_matricula_usuario:
                self.sistema.mapa_matricula_usuario.pop(matricula)
            self.sistema.lista_usuarios.remover_por_matricula(matricula)
            self.sistema.salvar_dados()
            self.atualizar_lista_usuarios()
            Messagebox.show_info("Usuário excluído com sucesso.", "Sucesso")

    # ==== RESTANTE IGUAL ====
    def criar_aba_emprestimos(self):
        frame = self.frame_emprestimos
        tb.Label(frame, text="Empréstimo e Devolução de Livros", font=("Segoe UI", 16, "bold")).pack(pady=10)
        form_emprestimo = tb.Frame(frame)
        form_emprestimo.pack(pady=10)
        tb.Label(form_emprestimo, text="Empréstimo - Matrícula:").grid(row=0, column=0, padx=5, pady=5)
        tb.Label(form_emprestimo, text="ISBN do Livro:").grid(row=1, column=0, padx=5, pady=5)
        self.emprestimo_matricula_var = tk.StringVar()
        self.emprestimo_isbn_var = tk.StringVar()
        tb.Entry(form_emprestimo, textvariable=self.emprestimo_matricula_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        tb.Entry(form_emprestimo, textvariable=self.emprestimo_isbn_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        tb.Button(form_emprestimo, text="Solicitar Empréstimo", bootstyle="success", command=self.solicitar_emprestimo).grid(row=2, column=0, columnspan=2, pady=10)
        tb.Label(form_emprestimo, text="Devolução - Matrícula:").grid(row=3, column=0, padx=5, pady=5)
        tb.Label(form_emprestimo, text="ISBN do Livro:").grid(row=4, column=0, padx=5, pady=5)
        self.devolucao_matricula_var = tk.StringVar()
        self.devolucao_isbn_var = tk.StringVar()
        tb.Entry(form_emprestimo, textvariable=self.devolucao_matricula_var, width=20).grid(row=3, column=1, padx=5, pady=5)
        tb.Entry(form_emprestimo, textvariable=self.devolucao_isbn_var, width=20).grid(row=4, column=1, padx=5, pady=5)
        tb.Button(form_emprestimo, text="Registrar Devolução", bootstyle="warning", command=self.registrar_devolucao).grid(row=5, column=0, columnspan=2, pady=10)
        tb.Label(frame, text="Consultar Fila de Espera de um Livro", font=("Segoe UI", 12, "bold")).pack(pady=10)
        consulta_frame = tb.Frame(frame)
        consulta_frame.pack(pady=5)
        self.consulta_fila_isbn_var = tk.StringVar()
        tb.Label(consulta_frame, text="ISBN do Livro:").grid(row=0, column=0, padx=5)
        tb.Entry(consulta_frame, textvariable=self.consulta_fila_isbn_var, width=20).grid(row=0, column=1, padx=5)
        tb.Button(consulta_frame, text="Ver Fila de Espera", bootstyle="info", command=self.ver_fila_espera).grid(row=0, column=2, padx=5)
        self.fila_espera_result = tk.Text(frame, height=4, width=60)
        self.fila_espera_result.pack(pady=5)

    def solicitar_emprestimo(self):
        matricula = self.emprestimo_matricula_var.get()
        isbn = self.emprestimo_isbn_var.get()
        sucesso, msg = self.sistema.realizar_emprestimo(matricula, isbn)
        self.sistema.salvar_dados()
        if sucesso:
            Messagebox.show_info(msg, "Empréstimo")
        else:
            Messagebox.show_error(msg, "Empréstimo")

    def registrar_devolucao(self):
        matricula = self.devolucao_matricula_var.get()
        isbn = self.devolucao_isbn_var.get()
        sucesso, msg = self.sistema.realizar_devolucao(matricula, isbn)
        self.sistema.salvar_dados()
        if sucesso:
            Messagebox.show_info(msg, "Devolução")
        else:
            Messagebox.show_error(msg, "Devolução")

    def ver_fila_espera(self):
        isbn = self.consulta_fila_isbn_var.get()
        livro = self.sistema.mapa_isbn_livro.get(isbn)
        self.fila_espera_result.delete(1.0, tk.END)
        if not livro:
            self.fila_espera_result.insert(tk.END, "Livro não encontrado.\n")
        elif livro.fila_espera.esta_vazia():
            self.fila_espera_result.insert(tk.END, "Sem fila de espera para esse livro.\n")
        else:
            self.fila_espera_result.insert(tk.END, "Fila de Espera:\n")
            for usuario in livro.fila_espera._dados:
                self.fila_espera_result.insert(tk.END, f"{usuario.nome} (Matrícula: {usuario.matricula})\n")

    def criar_aba_historico(self):
        frame = self.frame_historico
        tb.Label(frame, text="Histórico de Empréstimos", font=("Segoe UI", 16, "bold")).pack(pady=10)
        self.historico_text = tk.Text(frame, height=20, width=70)
        self.historico_text.pack(pady=10)
        tb.Button(frame, text="Atualizar Histórico", bootstyle="info", command=self.exibir_historico).pack(pady=5)
        self.btn_limpar_historico = tb.Button(
            frame,
            text="Limpar Histórico de Empréstimos",
            bootstyle="danger",
            command=self.limpar_historico
        )
        self.btn_limpar_historico.pack(pady=5)
        if self.usuario_logado and self.usuario_logado.tipo == "Funcionario":
            self.btn_limpar_historico.config(state=tk.NORMAL)
        else:
            self.btn_limpar_historico.config(state=tk.DISABLED)

    def exibir_historico(self):
        self.historico_text.delete(1.0, tk.END)
        historico = self.sistema.historico_emprestimos.get_all_items()
        if not historico:
            self.historico_text.insert(tk.END, "Nenhum empréstimo registrado.\n")
        else:
            for emprestimo in historico:
                self.historico_text.insert(tk.END, str(emprestimo) + "\n")

    def limpar_historico(self):
        resposta = Messagebox.okcancel("Tem certeza que deseja limpar o histórico de empréstimos?", "Confirmar")
        if resposta:
            self.sistema.limpar_historico_emprestimos()
            self.exibir_historico()
            Messagebox.show_info("Histórico limpo com sucesso!", "Limpar Histórico")

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = BibliotecaApp(root)
    root.mainloop()
