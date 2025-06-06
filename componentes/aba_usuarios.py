import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

class AbaUsuarios(tb.Frame):
    def __init__(self, master, sistema, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sistema = sistema
        self.configure(padding=18)

        tb.Label(self, text="👥 Usuários", font=("Segoe UI", 19, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 16))

        # SCROLLABLE CARDS
        self.cards_canvas = tk.Canvas(self, bg="#232629", highlightthickness=0, borderwidth=0, relief="flat")
        self.cards_frame = tb.Frame(self.cards_canvas)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.cards_canvas.yview)
        self.cards_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.cards_canvas.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="y", side="right")
        self.cards_canvas.create_window((0, 0), window=self.cards_frame, anchor="nw")
        self.cards_frame.bind("<Configure>", lambda e: self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all")))

        tb.Separator(self, orient="horizontal").pack(fill="x", pady=14)

        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=7)
        tb.Button(btn_frame, text="Atualizar", bootstyle="secondary-outline", width=12, command=self.mostrar_cards_usuarios).pack(side="left", padx=4)
        tb.Button(btn_frame, text="Novo", bootstyle="success-outline", width=12, command=self.mostrar_form_usuario).pack(side="left", padx=4)

        # Formulário de cadastro/edição de usuários
        self.frame_form_usuario = tb.Frame(self, padding=10)
        tb.Label(self.frame_form_usuario, text="Cadastro/Edição de Usuário", font=("Segoe UI", 15, "bold"), bootstyle="inverse-dark").pack(pady=(0, 8))

        form = tb.Frame(self.frame_form_usuario)
        form.pack(pady=5)
        labels = ["Nome:", "Matrícula:", "Curso:", "Tipo:", "Senha:"]
        self.entries = []
        for i, label in enumerate(labels):
            tb.Label(form, text=label, font=("Segoe UI", 11)).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            if label == "Tipo:":
                entry = tb.Combobox(form, values=["Cliente", "Funcionario"], state="readonly", width=35)
                entry.set("Cliente")
            else:
                entry = tb.Entry(form, width=38, font=("Segoe UI", 11), show="*" if label == "Senha:" else "")
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            self.entries.append(entry)
        self.nome_var, self.matricula_var, self.curso_var, self.tipo_var, self.senha_var = self.entries

        btns = tb.Frame(self.frame_form_usuario)
        btns.pack(pady=(14, 0))
        tb.Button(btns, text="Salvar", bootstyle="success", width=12, command=self.salvar_usuario).pack(side="left", padx=6)
        tb.Button(btns, text="Cancelar", bootstyle="secondary", width=12, command=self.mostrar_cards_usuarios).pack(side="left", padx=6)

        self.mostrar_cards_usuarios()
        self.editando_usuario_matricula = None

    def mostrar_form_usuario(self):
        self.cards_canvas.pack_forget()
        self.scrollbar.pack_forget()
        self.frame_form_usuario.pack(fill="x", pady=24)

    def mostrar_cards_usuarios(self):
        self.frame_form_usuario.pack_forget()
        self.cards_canvas.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="y", side="right")
        self.editando_usuario_matricula = None
        self._atualizar_cards_usuarios()

    def _atualizar_cards_usuarios(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        usuarios = self.sistema.lista_usuarios.listar_todos()
        if not usuarios:
            tb.Label(self.cards_frame, text="Nenhum usuário cadastrado.", font=("Segoe UI", 13), bootstyle="secondary").pack(pady=30)
            return

        for usuario in usuarios:
            card = tb.Frame(
                self.cards_frame,
                bootstyle="dark",
                padding=16,
                relief="raised",
                borderwidth=2
            )
            card.pack(fill="x", expand=True, pady=10, padx=8)

            tb.Label(card, text=usuario.nome, font=("Segoe UI", 14, "bold"), bootstyle="inverse-dark").pack(anchor="w")
            tb.Label(card, text=f"Matrícula: {usuario.matricula}", font=("Segoe UI", 11)).pack(anchor="w", pady=(2, 0))
            tb.Label(card, text=f"Curso: {usuario.curso}", font=("Segoe UI", 11)).pack(anchor="w")
            tb.Label(card, text=f"Tipo: {usuario.tipo}", font=("Segoe UI", 11)).pack(anchor="w", pady=(0, 2))

            # Botões de ação
            btns = tb.Frame(card, bootstyle="dark")
            btns.pack(anchor="e", pady=(4, 0))
            tb.Button(btns, text="Editar", bootstyle="warning-outline", width=8,
                      command=lambda u=usuario: self.abrir_edicao_usuario(u)).pack(side="left", padx=3)
            tb.Button(btns, text="Excluir", bootstyle="danger-outline", width=8,
                      command=lambda u=usuario: self.confirmar_exclusao_usuario(u)).pack(side="left", padx=3)

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
        self.nome_var.delete(0, tk.END)
        self.matricula_var.delete(0, tk.END)
        self.curso_var.delete(0, tk.END)
        self.tipo_var.set("Cliente")
        self.senha_var.delete(0, tk.END)
        self.mostrar_cards_usuarios()

    def abrir_edicao_usuario(self, usuario):
        self.nome_var.delete(0, tk.END)
        self.matricula_var.delete(0, tk.END)
        self.curso_var.delete(0, tk.END)
        self.senha_var.delete(0, tk.END)
        self.nome_var.insert(0, usuario.nome)
        self.matricula_var.insert(0, usuario.matricula)
        self.curso_var.insert(0, usuario.curso)
        self.tipo_var.set(usuario.tipo)
        self.senha_var.insert(0, usuario.senha)
        self.editando_usuario_matricula = usuario.matricula
        self.mostrar_form_usuario()

    def confirmar_exclusao_usuario(self, usuario):
        if usuario.matricula == "root":
            Messagebox.show_error("Não é permitido excluir o usuário root.", "Erro")
            return
        if Messagebox.okcancel(f"Tem certeza que deseja excluir o usuário de matrícula {usuario.matricula}?", "Confirmar exclusão"):
            if usuario.matricula in self.sistema.mapa_matricula_usuario:
                self.sistema.mapa_matricula_usuario.pop(usuario.matricula)
            self.sistema.lista_usuarios.remover_por_matricula(usuario.matricula)
            self.sistema.salvar_dados()
            self.mostrar_cards_usuarios()
            Messagebox.show_info("Usuário excluído com sucesso.", "Sucesso")
