import json
import datetime
import os
from estruturas_elementares import Livro, Usuario, Emprestimo, Fila, Pilha
from arvore_binaria_busca import ArvoreBinariaBusca
from lista_encadeada import ListaEncadeada

class SistemaBiblioteca:
    def __init__(self, arquivo_dados="minha_biblioteca.json"):
        self.arvore_livros_por_titulo = ArvoreBinariaBusca()
        self.mapa_isbn_livro = {}
        self.lista_usuarios = ListaEncadeada()
        self.mapa_matricula_usuario = {}
        self.historico_emprestimos = Pilha()
        self.arquivo_dados = arquivo_dados
        self.contador_id_livro = 1
        self.contador_matricula = 1
        self.carregar_dados()

    def cadastrar_livro(self, titulo, autor, isbn, quantidade):
        id_livro = str(self.contador_id_livro)
        self.contador_id_livro += 1
        if isbn in self.mapa_isbn_livro:
            print(f"Erro: Livro com ISBN {isbn} já cadastrado.")
            return False
        novo_livro = Livro(id_livro, titulo, autor, isbn, quantidade)
        self.arvore_livros_por_titulo.inserir(novo_livro)
        self.mapa_isbn_livro[isbn] = novo_livro
        return True

    def cadastrar_usuario(self, nome, curso, tipo="Cliente", senha=""):
        matricula = str(self.contador_matricula)
        self.contador_matricula += 1
        if matricula in self.mapa_matricula_usuario:
            print(f"Erro: Usuário com matrícula {matricula} já cadastrado.")
            return False
        novo_usuario = Usuario(nome, matricula, curso, tipo, senha)
        self.lista_usuarios.inserir_no_inicio(novo_usuario)
        self.mapa_matricula_usuario[matricula] = novo_usuario
        print(f"Usuário '{nome}' ({tipo}) cadastrado com sucesso! Matrícula: {matricula}")
        return True

    def _get_usuario_por_matricula(self, matricula):
        return self.mapa_matricula_usuario.get(matricula)

    def autenticar_usuario(self, matricula, senha):
        usuario = self.mapa_matricula_usuario.get(matricula)
        if usuario and usuario.senha == senha:
            return usuario
        return None

    def realizar_emprestimo(self, matricula_usuario, isbn_livro):
        usuario = self._get_usuario_por_matricula(matricula_usuario)
        livro = self.mapa_isbn_livro.get(isbn_livro)
        if usuario is None:
            print(f"Usuário com matrícula {matricula_usuario} não encontrado.")
            return False, "Usuário não encontrado."
        if livro is None:
            print(f"Livro com ISBN {isbn_livro} não encontrado.")
            return False, "Livro não encontrado."
        if livro.quantidade_exemplares > 0:
            livro.quantidade_exemplares -= 1
            emprestimo = Emprestimo(usuario, livro)
            self.historico_emprestimos.empilhar(emprestimo)
            print(f"Empréstimo realizado com sucesso para {usuario.nome}.")
            return True, "Empréstimo realizado com sucesso!"
        else:
            if matricula_usuario in livro.fila_espera.to_list_of_user_ids():
                print(f"Usuário {usuario.nome} já está na fila de espera para esse livro.")
                return False, "Usuário já está na fila de espera."
            livro.fila_espera.enfileirar(usuario)
            print(f"Livro indisponível. Usuário {usuario.nome} adicionado à fila de espera.")
            return False, "Livro indisponível. Usuário adicionado à fila de espera."

    def realizar_devolucao(self, matricula_usuario, isbn_livro):
        usuario = self._get_usuario_por_matricula(matricula_usuario)
        livro = self.mapa_isbn_livro.get(isbn_livro)
        if usuario is None:
            print(f"Usuário com matrícula {matricula_usuario} não encontrado.")
            return False, "Usuário não encontrado."
        if livro is None:
            print(f"Livro com ISBN {isbn_livro} não encontrado.")
            return False, "Livro não encontrado."
        livro.quantidade_exemplares += 1
        devolucao = Emprestimo(usuario, livro, data_emprestimo=datetime.date.today(), data_devolucao=datetime.date.today())
        self.historico_emprestimos.empilhar(devolucao)
        if not livro.fila_espera.esta_vazia():
            prox_usuario = livro.fila_espera.desenfileirar()
            livro.quantidade_exemplares -= 1
            novo_emprestimo = Emprestimo(prox_usuario, livro)
            self.historico_emprestimos.empilhar(novo_emprestimo)
            print(f"Livro foi automaticamente emprestado ao próximo da fila: {prox_usuario.nome}")
            return True, f"Devolução registrada. Livro automaticamente emprestado para {prox_usuario.nome}."
        print(f"Devolução registrada com sucesso.")
        return True, "Devolução registrada com sucesso."

    def consultar_usuario_por_matricula(self, matricula):
        usuario = self._get_usuario_por_matricula(matricula)
        if usuario:
            print(usuario)
        else:
            print(f"Usuário com matrícula {matricula} não encontrado.")
        return usuario

    def limpar_historico_emprestimos(self):
        self.historico_emprestimos = Pilha()
        self.salvar_dados()
        print("Histórico de empréstimos limpo com sucesso!")
        return True

    def salvar_dados(self):
        print(f"Salvando dados em {self.arquivo_dados}...")
        usuarios_data = [user.to_dict() for user in self.mapa_matricula_usuario.values()]
        livros_data = [livro.to_dict() for livro in self.mapa_isbn_livro.values()]
        historico_data = [emprestimo.to_dict() for emprestimo in self.historico_emprestimos.get_all_items()]
        dados_completos = {
            "usuarios": usuarios_data,
            "livros": livros_data,
            "historico_emprestimos": historico_data,
            "contador_id_livro": self.contador_id_livro,
            "contador_matricula": self.contador_matricula,
        }
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(dados_completos, f, ensure_ascii=False, indent=4)
            print("Dados salvos com sucesso!")
        except IOError as e:
            print(f"Erro ao salvar dados: {e}")

    def carregar_dados(self):
        if not os.path.exists(self.arquivo_dados):
            print(f"Arquivo de dados '{self.arquivo_dados}' não encontrado. Começando com sistema vazio.")
            # --- Criação automática do usuário root caso não exista o arquivo ---
            self.cadastrar_usuario("Administrador", "ADM", "Funcionario", "admin")
            self.salvar_dados()
            return

        print(f"Carregando dados de {self.arquivo_dados}...")
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados_completos = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar dados: {e}. Começando com sistema vazio.")
            # --- Criação automática do usuário root caso arquivo corrompido ---
            self.cadastrar_usuario("Administrador", "ADM", "Funcionario", "admin")
            self.salvar_dados()
            return

        self.arvore_livros_por_titulo = ArvoreBinariaBusca()
        self.mapa_isbn_livro.clear()
        self.lista_usuarios = ListaEncadeada()
        self.mapa_matricula_usuario.clear()
        self.historico_emprestimos = Pilha()
        for user_data in dados_completos.get("usuarios", []):
            usuario = Usuario.from_dict(user_data)
            self.lista_usuarios.inserir_no_inicio(usuario)
            self.mapa_matricula_usuario[usuario.matricula] = usuario
        for livro_data in dados_completos.get("livros", []):
            livro = Livro.from_dict(livro_data, self.mapa_matricula_usuario)
            self.arvore_livros_por_titulo.inserir(livro)
            self.mapa_isbn_livro[livro.isbn] = livro
        for emprestimo_data in dados_completos.get("historico_emprestimos", []):
            emprestimo = Emprestimo.from_dict(emprestimo_data, self.mapa_matricula_usuario, self.mapa_isbn_livro)
            if emprestimo:
                self.historico_emprestimos.empilhar(emprestimo)
        print("Dados carregados com sucesso!")

        # --- Criação automática do usuário root se não houver nenhum usuário no sistema ---
        if not self.mapa_matricula_usuario:
            print("Nenhum usuário encontrado. Criando usuário root padrão (matrícula: root, senha: admin).")
            self.cadastrar_usuario("Administrador", "ADM", "Funcionario", "admin")
            self.salvar_dados()

    def listar_todos_os_livros(self):
        livros = self.arvore_livros_por_titulo.listar_todos_em_ordem()
        if not livros:
            print("Nenhum livro cadastrado.")
            return
        print("\n--- Lista de Livros (ordenados por título) ---")
        for livro in livros:
            print(f"Título: {livro.titulo} | Autor: {livro.autor} | ISBN: {livro.isbn} | Quantidade: {livro.quantidade_exemplares}")

    def listar_todos_os_usuarios(self):
        usuarios = self.mapa_matricula_usuario.values()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return
        print("\n--- Lista de Usuários ---")
        for usuario in usuarios:
            print(f"Nome: {usuario.nome} | Matrícula: {usuario.matricula} | Curso: {usuario.curso} | Tipo: {usuario.tipo}")

