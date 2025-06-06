class NoArvore:
    def __init__(self, livro):
        self.livro = livro
        self.esquerda = None
        self.direita = None
        self.chave = livro.titulo.lower()

class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    def inserir(self, livro):
        if self.raiz is None:
            self.raiz = NoArvore(livro)
        else:
            self._inserir_recursivo(self.raiz, livro)

    def _inserir_recursivo(self, no_atual, livro):
        chave_livro = livro.titulo.lower()
        if chave_livro < no_atual.chave:
            if no_atual.esquerda is None:
                no_atual.esquerda = NoArvore(livro)
            else:
                self._inserir_recursivo(no_atual.esquerda, livro)
        elif chave_livro > no_atual.chave:
            if no_atual.direita is None:
                no_atual.direita = NoArvore(livro)
            else:
                self._inserir_recursivo(no_atual.direita, livro)
        else:
            # Títulos iguais: sobrepõe quantidade se ISBN também igual
            if no_atual.livro.isbn == livro.isbn:
                no_atual.livro.quantidade_exemplares = livro.quantidade_exemplares
            else:
                print(f"Aviso: Título '{livro.titulo}' já existe com ISBN diferente. Não inserido.")

    def buscar(self, titulo):
        return self._buscar_recursivo(self.raiz, titulo.lower())

    def _buscar_recursivo(self, no_atual, titulo_busca):
        if no_atual is None or no_atual.chave == titulo_busca:
            return no_atual.livro if no_atual else None
        if titulo_busca < no_atual.chave:
            return self._buscar_recursivo(no_atual.esquerda, titulo_busca)
        else:
            return self._buscar_recursivo(no_atual.direita, titulo_busca)

    def buscar_por_isbn(self, isbn):
        return self._buscar_isbn_recursivo(self.raiz, isbn)

    def _buscar_isbn_recursivo(self, no_atual, isbn):
        if no_atual is None:
            return None
        if no_atual.livro.isbn == isbn:
            return no_atual.livro
        res = self._buscar_isbn_recursivo(no_atual.esquerda, isbn)
        if res:
            return res
        return self._buscar_isbn_recursivo(no_atual.direita, isbn)

    def listar_todos_em_ordem(self):
        livros = []
        self._listar_todos_em_ordem_recursivo(self.raiz, livros)
        return livros

    def _listar_todos_em_ordem_recursivo(self, no_atual, livros):
        if no_atual:
            self._listar_todos_em_ordem_recursivo(no_atual.esquerda, livros)
            livros.append(no_atual.livro)
            self._listar_todos_em_ordem_recursivo(no_atual.direita, livros)

    # REMOÇÃO POR ISBN ROBUSTA (procura em toda árvore!)
    def remover(self, isbn):
        def remover_rec(no):
            if not no:
                return None, False
            # Busca pelo ISBN em qualquer nó, não pela ordenação!
            if no.livro.isbn == isbn:
                # Encontrou: 3 casos
                if not no.esquerda:
                    return no.direita, True
                if not no.direita:
                    return no.esquerda, True
                # Nó com dois filhos: substitui pelo menor da direita
                temp = no.direita
                while temp.esquerda:
                    temp = temp.esquerda
                no.livro = temp.livro
                no.chave = temp.chave
                no.direita, _ = remover_rec_no_isbn(no.direita, temp.livro.isbn)
                return no, True
            # Recursivamente procura nos dois lados
            no.esquerda, removed_esq = remover_rec(no.esquerda)
            if removed_esq:
                return no, True
            no.direita, removed_dir = remover_rec(no.direita)
            return no, removed_dir

        def remover_rec_no_isbn(no, isbn_busca):
            if not no:
                return None, False
            if no.livro.isbn == isbn_busca:
                if not no.esquerda:
                    return no.direita, True
                if not no.direita:
                    return no.esquerda, True
                temp = no.direita
                while temp.esquerda:
                    temp = temp.esquerda
                no.livro = temp.livro
                no.chave = temp.chave
                no.direita, _ = remover_rec_no_isbn(no.direita, temp.livro.isbn)
                return no, True
            no.esquerda, removed_esq = remover_rec_no_isbn(no.esquerda, isbn_busca)
            if removed_esq:
                return no, True
            no.direita, removed_dir = remover_rec_no_isbn(no.direita, isbn_busca)
            return no, removed_dir

        self.raiz, _ = remover_rec(self.raiz)
