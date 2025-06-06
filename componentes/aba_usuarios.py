import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

class AbaUsuarios(tb.Frame):
    def __init__(self, master, sistema, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sistema = sistema
        self.configure(padding=18)

        # Título da aba
        tb.Label(self, text="👥 Usuários", font=("Segoe UI", 19, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 16))

        # Listbox de usuários
        self.usuarios_listbox = tk.Listbox(self, width=70, height=15, font=("Segoe UI", 11))
        self.usuarios_listbox.pack(pady=8, fill="x")

        tb.Separator(self, orient="horizontal").pack(fill="x", pady=14)

        # Botões principais
        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=7)
        tb.Button(btn_frame, text="Atualizar", bootstyle="secondary-outline", width=12, command=self.atualizar_lista_usuarios).pack(side="left", padx=4)
        tb.Button(btn_frame, text="Novo", bootstyle="success-outline", width=12, command=self.mostrar_form_usuario).pack(side="left", padx=4)
        tb.Button(btn_frame, text="Editar", bootstyle="warning-outline", width=12, command=self.editar_usuario_selecionado).pack(side="left", padx=4)
        tb.Button(btn_frame, text="Excluir", bootstyle="danger-outline", width=12, command=self.excluir_usuario_selecionado).pack(side="left", padx=4)

        # Formulário de cadastro/edição
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
        tb.Button(btns, text="Cancelar", bootstyle="secondary", width=12, command=self.mostrar_lista_usuarios).pack(side="left", padx=6)

        self.mostrar_lista_usuarios()
        self.editando_usuario_matricula = None

    def mostrar_form_usuario(self):
        self.usuarios_listbox.pack_forget()
        self.frame_form_usuario.pack(fill="x", pady=24)

    def mostrar_lista_usuarios(self):
        self.frame_form_usuario.pack_forget()
        self.usuarios_listbox.pack(pady=8, fill="x")
        self.atualizar_lista_usuarios()
        self.editando_usuario_matricula = None

    def atualizar_lista_usuarios(self):
        self.usuarios_listbox.delete(0, tk.END)
        usuarios = self.sistema.lista_usuarios.listar_todos()
        for usuario in usuarios:
            self.usuarios_listbox.insert(
                tk.END,
                f"{usuario.nome} | {usuario.matricula} | {usuario.curso} | {usuario.tipo}"
            )

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
        self.mostrar_lista_usuarios()

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
        self.nome_var.delete(0, tk.END)
        self.matricula_var.delete(0, tk.END)
        self.curso_var.delete(0, tk.END)
        self.senha_var.delete(0, tk.END)
        self.nome_var.insert(0, usuario.nome)
        self.matricula_var.insert(0, usuario.matricula)
        self.curso_var.insert(0, usuario.curso)
        self.tipo_var.set(usuario.tipo)
        self.senha_var.insert(0, usuario.senha)
        self.editando_usuario_matricula = matricula
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
