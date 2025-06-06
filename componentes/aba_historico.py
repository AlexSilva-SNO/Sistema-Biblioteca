import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.dialogs import Messagebox

class AbaHistorico(tb.Frame):
    def __init__(self, master, sistema, usuario_logado, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.sistema = sistema
        self.usuario_logado = usuario_logado
        self.configure(padding=18)

        tb.Label(self, text="📜 Histórico de Empréstimos", font=("Segoe UI", 19, "bold"), bootstyle="inverse-dark").pack(anchor="w", pady=(0, 14))

        # Textbox para exibir histórico
        self.historico_text = tk.Text(self, height=19, width=90, font=("Segoe UI", 11), state=tk.DISABLED, wrap="word", bg="#232629", fg="#eee", bd=0, relief="flat")
        self.historico_text.pack(pady=8, fill="both", expand=True)

        tb.Separator(self, orient="horizontal").pack(fill="x", pady=12)

        btn_frame = tb.Frame(self)
        btn_frame.pack(pady=4)

        tb.Button(btn_frame, text="Atualizar Histórico", bootstyle="secondary-outline", width=16, command=self.exibir_historico).pack(side="left", padx=4)
        
        # Limpar histórico só para funcionários
        self.btn_limpar_historico = tb.Button(
            btn_frame,
            text="Limpar Histórico",
            bootstyle="danger-outline",
            width=16,
            command=self.limpar_historico
        )
        self.btn_limpar_historico.pack(side="left", padx=4)

        if self.usuario_logado.tipo == "Funcionario":
            self.btn_limpar_historico.config(state=tk.NORMAL)
        else:
            self.btn_limpar_historico.config(state=tk.DISABLED)

        self.exibir_historico()

    def exibir_historico(self):
        self.historico_text.config(state=tk.NORMAL)
        self.historico_text.delete(1.0, tk.END)
        historico = self.sistema.historico_emprestimos.get_all_items()
        if not historico:
            self.historico_text.insert(tk.END, "Nenhum empréstimo registrado.\n")
        else:
            for emprestimo in historico:
                self.historico_text.insert(tk.END, str(emprestimo) + "\n")
        self.historico_text.config(state=tk.DISABLED)

    def limpar_historico(self):
        if Messagebox.okcancel("Tem certeza que deseja limpar o histórico de empréstimos?", "Confirmar"):
            self.sistema.limpar_historico_emprestimos()
            self.exibir_historico()
            Messagebox.show_info("Histórico limpo com sucesso!", "Limpar Histórico")
