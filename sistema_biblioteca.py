# sistema_biblioteca.py
import json
import datetime
import os # Para verificar se o arquivo existe
from estruturas_elementares import Livro, Usuario, Emprestimo, Fila, Pilha
from arvore_binaria_busca import ArvoreBinariaBusca
from lista_encadeada import ListaEncadeada # Supondo que você tenha métodos para iterar ou obter todos

class SistemaBiblioteca:
    def __init__(self, arquivo_dados="dados_biblioteca.json"):
        self.arvore_livros_por_titulo = ArvoreBinariaBusca()
        self.mapa_isbn_livro = {}
        self.lista_usuarios = ListaEncadeada() # Sua lista encadeada
        self.mapa_matricula_usuario = {} # Adicionado para acesso rápido ao carregar
        self.historico_emprestimos = Pilha()
        self.arquivo_dados = arquivo_dados
        self.carregar_dados() # Tenta carregar ao iniciar


    def cadastrar_livro(self, titulo, autor, isbn, quantidade):
        if isbn in self.mapa_isbn_livro:
            # ... (lógica existente) ...
            return False
        
        novo_livro = Livro(titulo, autor, isbn, quantidade)
        self.arvore_livros_por_titulo.inserir(novo_livro)
        self.mapa_isbn_livro[isbn] = novo_livro
        # A ABB já imprime avisos de título duplicado
        return True

    def cadastrar_usuario(self, nome, matricula, curso):
        if matricula in self.mapa_matricula_usuario: # Verifica no mapa para O(1)
            print(f"Erro: Usuário com matrícula {matricula} já cadastrado.")
            return False
        novo_usuario = Usuario(nome, matricula, curso)
        self.lista_usuarios.inserir_no_inicio(novo_usuario) # Ou onde preferir
        self.mapa_matricula_usuario[matricula] = novo_usuario # Mantém o mapa atualizado
        print(f"Usuário '{nome}' cadastrado com sucesso!")
        return True
    
    # ... (realizar_emprestimo, realizar_devolucao, consultas, etc., permanecem os mesmos) ...
    # Apenas garanta que buscar_por_matricula e buscar_por_isbn usem os mapas para eficiência
    # Na versão anterior, buscar_por_matricula já estava na ListaEncadeada.
    # Se quiser usar o mapa_matricula_usuario consistentemente:
    def _get_usuario_por_matricula(self, matricula): # Método interno
        return self.mapa_matricula_usuario.get(matricula)

    def realizar_emprestimo(self, matricula_usuario, isbn_livro):
        usuario = self._get_usuario_por_matricula(matricula_usuario)
        # ... resto da função ...

    def realizar_devolucao(self, matricula_usuario, isbn_livro):
        usuario = self._get_usuario_por_matricula(matricula_usuario)
        # ... resto da função ...
    
    def consultar_usuario_por_matricula(self, matricula):
        usuario = self._get_usuario_por_matricula(matricula)
        if usuario:
            print(usuario)
        else:
            print(f"Usuário com matrícula {matricula} não encontrado.")
        return usuario


    def salvar_dados(self):
        print(f"Salvando dados em {self.arquivo_dados}...")
        # Coletar todos os usuários
        usuarios_data = [user.to_dict() for user in self.mapa_matricula_usuario.values()]
        
        # Coletar todos os livros
        livros_data = [livro.to_dict() for livro in self.mapa_isbn_livro.values()]
        
        # Coletar histórico de empréstimos
        # A pilha precisa de um método para obter todos os itens sem desempilhar
        # ou iterar sobre ela. Adicionei get_all_items() à classe Pilha.
        historico_data = [emprestimo.to_dict() for emprestimo in self.historico_emprestimos.get_all_items()]

        dados_completos = {
            "usuarios": usuarios_data,
            "livros": livros_data,
            "historico_emprestimos": historico_data,
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
            return

        print(f"Carregando dados de {self.arquivo_dados}...")
        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                dados_completos = json.load(f)
        except (IOError, json.JSONDecodeError) as e:
            print(f"Erro ao carregar dados: {e}. Começando com sistema vazio.")
            return

        # Limpar estruturas atuais antes de carregar (se necessário)
        self.arvore_livros_por_titulo = ArvoreBinariaBusca()
        self.mapa_isbn_livro.clear()
        self.lista_usuarios = ListaEncadeada() # Recria a lista
        self.mapa_matricula_usuario.clear()
        self.historico_emprestimos = Pilha()

        # 1. Carregar Usuários e popular mapa_matricula_usuario
        for user_data in dados_completos.get("usuarios", []):
            usuario = Usuario.from_dict(user_data)
            self.lista_usuarios.inserir_no_inicio(usuario) # Ou outra forma de adicionar à sua lista
            self.mapa_matricula_usuario[usuario.matricula] = usuario
        
        # 2. Carregar Livros e reconstruir filas de espera
        for livro_data in dados_completos.get("livros", []):
            # Passa o mapa de usuários para que Livro.from_dict possa reconstruir a fila_espera
            livro = Livro.from_dict(livro_data, self.mapa_matricula_usuario)
            self.arvore_livros_por_titulo.inserir(livro)
            self.mapa_isbn_livro[livro.isbn] = livro
            
        # 3. Carregar Histórico de Empréstimos
        for emprestimo_data in dados_completos.get("historico_emprestimos", []):
            # Passa ambos os mapas para que Emprestimo.from_dict possa encontrar os objetos
            emprestimo = Emprestimo.from_dict(emprestimo_data, self.mapa_matricula_usuario, self.mapa_isbn_livro)
            if emprestimo: # Se foi possível reconstruir
                self.historico_emprestimos.empilhar(emprestimo)
        
        print("Dados carregados com sucesso!")

    def listar_todos_os_livros(self):
        livros = self.arvore_livros_por_titulo.listar_todos_em_ordem()  # Corrigido!
        if not livros:
            print("Nenhum livro cadastrado.")
            return
        print("\n--- Lista de Livros (ordenados por título) ---")
        for livro in livros:
            print(f"Título: {livro.titulo} | Autor: {livro.autor} | ISBN: {livro.isbn} | Quantidade: {livro.quantidade_exemplares}")