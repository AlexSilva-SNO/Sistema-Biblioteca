import tkinter as tk

class AbaVisualizacaoLista(tk.Frame):
    def __init__(self, master, sistema):
        super().__init__(master)
        self.sistema = sistema

        self.btn_carregar = tk.Button(self, text="Carregar", command=self.atualizar_visualizacao)
        self.btn_carregar.pack(pady=5)

        self.canvas = tk.Canvas(self, bg="white", width=950, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.atualizar_visualizacao()

    def atualizar_visualizacao(self):
        self.canvas.delete("all")
        usuarios = self.sistema.lista_usuarios.listar_todos()
        if not usuarios:
            self.canvas.create_text(475, 300, text="Nenhum usuário cadastrado.", font=("Arial", 16), fill="gray")
            return

        x, y = 100, 50
        for i, usuario in enumerate(usuarios, 1):
            texto = f"{i}. {usuario.nome} ({usuario.matricula}) - {usuario.curso} [{usuario.tipo}]"
            self.canvas.create_text(x, y, text=texto, anchor="w", font=("Arial", 12))
            y += 30