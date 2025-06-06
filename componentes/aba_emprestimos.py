import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

class AbaEmprestimos(tb.Frame):
    def __init__(self, master, sistema, usuario_logado, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sistema = sistema
        self.usuario_logado = usuario_logado
        self.configure(padding=18)

        tb.Label(self, text="📦 Empréstimo & Devolução de Livros", font=("Segoe UI", 19, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 14))

        form_emprestimo = tb.Frame(self)
        form_emprestimo.pack(pady=10, fill="x")

        # Empréstimo
        tb.Label(form_emprestimo, text="Matrícula:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=4, pady=6, sticky="e")
        tb.Label(form_emprestimo, text="ISBN do Livro:", font=("Segoe UI", 11)).grid(row=1, column=0, padx=4, pady=6, sticky="e")
        self.emprestimo_matricula_var = tk.StringVar(value=usuario_logado.matricula if usuario_logado.tipo != "Funcionario" else "")
        self.emprestimo_isbn_var = tk.StringVar()
        tb.Entry(form_emprestimo, textvariable=self.emprestimo_matricula_var, width=22).grid(row=0, column=1, padx=4, pady=6)
        tb.Entry(form_emprestimo, textvariable=self.emprestimo_isbn_var, width=22).grid(row=1, column=1, padx=4, pady=6)
        tb.Button(form_emprestimo, text="Solicitar Empréstimo", bootstyle="success-outline", width=18, command=self.solicitar_emprestimo).grid(row=2, column=0, columnspan=2, pady=10)

        # Devolução
        tb.Label(form_emprestimo, text="Matrícula:", font=("Segoe UI", 11)).grid(row=3, column=0, padx=4, pady=6, sticky="e")
        tb.Label(form_emprestimo, text="ISBN do Livro:", font=("Segoe UI", 11)).grid(row=4, column=0, padx=4, pady=6, sticky="e")
        self.devolucao_matricula_var = tk.StringVar(value=usuario_logado.matricula if usuario_logado.tipo != "Funcionario" else "")
        self.devolucao_isbn_var = tk.StringVar()
        tb.Entry(form_emprestimo, textvariable=self.devolucao_matricula_var, width=22).grid(row=3, column=1, padx=4, pady=6)
        tb.Entry(form_emprestimo, textvariable=self.devolucao_isbn_var, width=22).grid(row=4, column=1, padx=4, pady=6)
        tb.Button(form_emprestimo, text="Registrar Devolução", bootstyle="warning-outline", width=18, command=self.registrar_devolucao).grid(row=5, column=0, columnspan=2, pady=10)

        tb.Separator(self, orient="horizontal").pack(fill="x", pady=14)

        # Consulta fila de espera
        consulta_frame = tb.Frame(self)
        consulta_frame.pack(pady=6, fill="x")
        tb.Label(consulta_frame, text="Consultar Fila de Espera do Livro", font=("Segoe UI", 13, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 8))

        frame_fila = tb.Frame(consulta_frame)
        frame_fila.pack()
        self.consulta_fila_isbn_var = tk.StringVar()
        tb.Label(frame_fila, text="ISBN do Livro:", font=("Segoe UI", 11)).grid(row=0, column=0, padx=4)
        tb.Entry(frame_fila, textvariable=self.consulta_fila_isbn_var, width=22).grid(row=0, column=1, padx=4)
        tb.Button(frame_fila, text="Ver Fila", bootstyle="info-outline", width=12, command=self.ver_fila_espera).grid(row=0, column=2, padx=4)
        self.fila_espera_result = tk.Text(consulta_frame, height=4, width=62, font=("Segoe UI", 11), bg="#232629", fg="#eee", bd=0, relief="flat")
        self.fila_espera_result.pack(pady=5, fill="x")

    def solicitar_emprestimo(self):
        matricula = self.emprestimo_matricula_var.get().strip()
        isbn = self.emprestimo_isbn_var.get().strip()
        if not matricula or not isbn:
            Messagebox.show_error("Informe matrícula e ISBN.", "Erro")
            return
        sucesso, msg = self.sistema.realizar_emprestimo(matricula, isbn)
        self.sistema.salvar_dados()
        if sucesso:
            Messagebox.show_info(msg, "Empréstimo")
        else:
            Messagebox.show_error(msg, "Empréstimo")

    def registrar_devolucao(self):
        matricula = self.devolucao_matricula_var.get().strip()
        isbn = self.devolucao_isbn_var.get().strip()
        if not matricula or not isbn:
            Messagebox.show_error("Informe matrícula e ISBN.", "Erro")
            return
        sucesso, msg = self.sistema.realizar_devolucao(matricula, isbn)
        self.sistema.salvar_dados()
        if sucesso:
            Messagebox.show_info(msg, "Devolução")
        else:
            Messagebox.show_error(msg, "Devolução")

    def ver_fila_espera(self):
        isbn = self.consulta_fila_isbn_var.get().strip()
        livro = self.sistema.mapa_isbn_livro.get(isbn)
        self.fila_espera_result.config(state=tk.NORMAL)
        self.fila_espera_result.delete(1.0, tk.END)
        if not livro:
            self.fila_espera_result.insert(tk.END, "Livro não encontrado.\n")
        elif livro.fila_espera.esta_vazia():
            self.fila_espera_result.insert(tk.END, "Sem fila de espera para esse livro.\n")
        else:
            self.fila_espera_result.insert(tk.END, "Fila de Espera:\n")
            for usuario in livro.fila_espera._dados:
                self.fila_espera_result.insert(tk.END, f"{usuario.nome} (Matrícula: {usuario.matricula})\n")
        self.fila_espera_result.config(state=tk.DISABLED)
