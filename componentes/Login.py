import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

class TelaLogin:
    def __init__(self, master, on_login):
        self.top = tk.Toplevel(master)
        self.top.title("Login - Biblioteca")
        self.top.geometry("450x300")
        self.top.resizable(False, False)
        self.top.grab_set()
        self.top.configure(bg="#222")  # fundo neutro/escuro

        self.on_login = on_login

        frame = tb.Frame(self.top, padding=24, bootstyle="dark")
        frame.pack(fill="both", expand=True)

        tb.Label(frame, text="Acesso ao Sistema", 
                 font=("Segoe UI", 15, "bold"), 
                 bootstyle="inverse-dark").pack(pady=(0, 16))

        tb.Label(frame, text="Matrícula:", font=("Segoe UI", 11), bootstyle="inverse-dark").pack(anchor="w")
        self.matricula_var = tk.StringVar()
        tb.Entry(frame, textvariable=self.matricula_var, width=15, font=("Segoe UI", 11)).pack(pady=(0,8))

        tb.Label(frame, text="Senha:", font=("Segoe UI", 11), bootstyle="inverse-dark").pack(anchor="w")
        self.senha_var = tk.StringVar()
        tb.Entry(frame, textvariable=self.senha_var, width=15, show="*", font=("Segoe UI", 11)).pack(pady=(0, 14))

        tb.Button(frame, text="Entrar", bootstyle="success", width=10, command=self.login).pack()

        # Atalho ENTER para login
        self.top.bind('<Return>', lambda e: self.login())

    def login(self):
        matricula = self.matricula_var.get().strip()
        senha = self.senha_var.get().strip()
        if not matricula or not senha:
            Messagebox.show_error("Preencha todos os campos!", "Erro")
            return
        self.on_login(matricula, senha, self.top)
