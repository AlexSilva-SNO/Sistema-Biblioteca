import datetime
from collections import deque

class Fila:
    def __init__(self):
        self._dados = deque()

    def enfileirar(self, item):
        self._dados.append(item)

    def desenfileirar(self):
        if not self.esta_vazia():
            return self._dados.popleft()
        return None

    def esta_vazia(self):
        return len(self._dados) == 0

    def ver_primeiro(self):
        if not self.esta_vazia():
            return self._dados[0]
        return None
    
    def __len__(self):
        return len(self._dados)
    
    def to_list_of_user_ids(self):
        if all(hasattr(user, "matricula") for user in self._dados):
            return [user.matricula for user in self._dados]
        return []

    def from_list_of_user_ids(self, user_ids, user_map):
        self._dados.clear()
        for user_id in user_ids:
            user = user_map.get(user_id)
            if user:
                self.enfileirar(user)

class Pilha:
    def __init__(self):
        self._dados = []

    def empilhar(self, item):
        self._dados.append(item)

    def desempilhar(self):
        if not self.esta_vazia():
            return self._dados.pop()
        return None

    def esta_vazia(self):
        return len(self._dados) == 0

    def ver_topo(self):
        if not self.esta_vazia():
            return self._dados[-1]
        return None
    
    def __iter__(self):
        return reversed(self._dados)
    
    def get_all_items(self):
        return list(self._dados)

class Usuario:
    def __init__(self, nome, matricula, curso, tipo="Cliente", senha=""):
        self.nome = nome
        self.matricula = matricula
        self.curso = curso
        self.tipo = tipo  # "Cliente" ou "Funcionario"
        self.senha = senha

    def __str__(self):
        return f"Nome: {self.nome}, Matrícula: {self.matricula}, Curso: {self.curso}, Tipo: {self.tipo}"

    def to_dict(self):
        return {
            "nome": self.nome,
            "matricula": self.matricula,
            "curso": self.curso,
            "tipo": self.tipo,
            "senha": self.senha
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["nome"],
            data["matricula"],
            data["curso"],
            data.get("tipo", "Cliente"),
            data.get("senha", "")
        )

class Livro:
    def __init__(self, id_livro, titulo, autor, isbn, quantidade_exemplares):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.quantidade_exemplares = quantidade_exemplares
        self.fila_espera = Fila()

    def __str__(self):
        return f"Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Disponíveis: {self.quantidade_exemplares}"

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "isbn": self.isbn,
            "quantidade_exemplares": self.quantidade_exemplares,
            "fila_espera_ids": self.fila_espera.to_list_of_user_ids(),
        }

    @classmethod
    def from_dict(cls, data, user_map):
        livro = cls(
            data["titulo"],
            data["autor"],
            data["isbn"],
            data["quantidade_exemplares"],
        )
        if "fila_espera_ids" in data:
            livro.fila_espera.from_list_of_user_ids(data["fila_espera_ids"], user_map)
        return livro

class Emprestimo:
    def __init__(self, usuario, livro, data_emprestimo=None, data_devolucao=None):
        self.usuario = usuario
        self.livro = livro
        self.data_emprestimo = data_emprestimo if data_emprestimo else datetime.date.today()
        self.data_devolucao = data_devolucao

    def __str__(self):
        status_devolucao = f"Devolvido em: {self.data_devolucao.isoformat()}" if self.data_devolucao else "Ainda emprestado"
        data_emp_str = self.data_emprestimo.isoformat() if isinstance(self.data_emprestimo, datetime.date) else str(self.data_emprestimo)

        return (f"Usuário: {self.usuario.nome} (Mat: {self.usuario.matricula})\n"
                f"Livro: {self.livro.titulo} (ISBN: {self.livro.isbn})\n"
                f"Emprestado em: {data_emp_str}\n"
                f"{status_devolucao}\n" + "-"*20)

    def to_dict(self):
        return {
            "matricula_usuario": self.usuario.matricula,
            "isbn_livro": self.livro.isbn,
            "data_emprestimo": self.data_emprestimo.isoformat() if isinstance(self.data_emprestimo, datetime.date) else str(self.data_emprestimo),
            "data_devolucao": self.data_devolucao.isoformat() if self.data_devolucao else None,
        }

    @classmethod
    def from_dict(cls, data, user_map, book_map):
        usuario = user_map.get(data["matricula_usuario"])
        livro = book_map.get(data["isbn_livro"])

        if not usuario or not livro:
            print(f"Aviso: Não foi possível reconstruir empréstimo para usuário {data['matricula_usuario']} ou livro {data['isbn_livro']}.")
            return None

        data_emprestimo = datetime.date.fromisoformat(data["data_emprestimo"])
        data_devolucao = datetime.date.fromisoformat(data["data_devolucao"]) if data["data_devolucao"] else None
        
        return cls(usuario, livro, data_emprestimo, data_devolucao)
