class NoLista:
    def __init__(self, usuario):
        self.usuario = usuario
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.cabeca = None

    def esta_vazia(self):
        return self.cabeca is None

    def inserir_no_inicio(self, usuario):
        novo_no = NoLista(usuario)
        novo_no.proximo = self.cabeca
        self.cabeca = novo_no

    def buscar_por_matricula(self, matricula):
        atual = self.cabeca
        while atual is not None:
            if atual.usuario.matricula == matricula:
                return atual.usuario  # Retorna o objeto, pronto para edição
            atual = atual.proximo
        return None

    def listar_todos(self):
        usuarios = []
        atual = self.cabeca
        while atual is not None:
            usuarios.append(atual.usuario)
            atual = atual.proximo
        return usuarios

    def remover_por_matricula(self, matricula):
        atual = self.cabeca
        anterior = None
        while atual is not None:
            if atual.usuario.matricula == matricula:
                if anterior is None:
                    self.cabeca = atual.proximo
                else:
                    anterior.proximo = atual.proximo
                return True  # Removido com sucesso
            anterior = atual
            atual = atual.proximo
        return False  # Não encontrado

    # Opcional: editar direto no objeto retornado por buscar_por_matricula
    # Exemplo de uso:
    # usuario = lista_encadeada.buscar_por_matricula("123")
    # if usuario:
    #     usuario.nome = "Novo Nome"
    #     usuario.senha = "novaSenha"
