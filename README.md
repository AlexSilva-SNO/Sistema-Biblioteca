# 🏛️ Sistema de Gerenciamento de Biblioteca 📚

Este projeto implementa um **Sistema de Gerenciamento de Biblioteca** em Python, com interface gráfica moderna, utilizando estruturas de dados clássicas e arquitetura modular. O sistema é ideal para fins acadêmicos, demonstração de conceitos de Estrutura de Dados e uso prático em pequenos ambientes de biblioteca.

---

## ✨ Funcionalidades Principais

### 1. Cadastro de Livros

* **Armazenamento:** Árvore Binária de Busca (ABB)
* **Campos:** Título, Autor, ISBN, Quantidade de exemplares disponíveis
* **Busca:** Por título (ABB) e ISBN (dicionário auxiliar)
* **Fila de Espera:** Cada livro possui uma fila de espera individual para reservas

### 2. Cadastro de Usuários

* **Armazenamento:** Lista Encadeada
* **Campos:** Nome, Matrícula, Curso, Tipo (Cliente ou Funcionário), Senha (login seguro)
* **Busca:** Por matrícula (lista encadeada)

### 3. Empréstimo de Livros

* **Verificação de disponibilidade:** Se houver exemplar, registra o empréstimo e atualiza a quantidade
* **Fila de Espera:** Se não houver exemplar, o usuário entra na fila de espera do livro

### 4. Devolução de Livros

* **Histórico:** Toda devolução é registrada em uma pilha de histórico de empréstimos
* **Liberação automática:** Se houver fila, o próximo usuário recebe o exemplar automaticamente

### 5. Consultas e Relatórios

* **Livros:** Busca por título e ISBN
* **Usuários:** Busca por matrícula
* **Histórico:** Consulta de todos os empréstimos e devoluções realizados
* **Fila de Espera:** Consulta dos próximos usuários aguardando cada livro

### 6. Controle de Permissões e Login

* **Login seguro:** Acesso ao sistema por matrícula e senha
* **Funcionário vs Cliente:** Apenas funcionários podem cadastrar/editar/excluir livros e usuários, além de limpar histórico

### 7. Interface Moderna

* **Interface gráfica:** Tkinter + ttkbootstrap
* **Visual:** Limpo, dark mode, responsivo, navegação por abas
* **Componentização:** Código dividido em arquivos por aba/tela (fácil manutenção e extensões)
* **Compilação para .exe:** Executável sem necessidade de Python instalado

---

## 🛠️ Estruturas de Dados Utilizadas

| Estrutura       | Utilização                                                    |
| --------------- | ------------------------------------------------------------- |
| ABB             | Armazenamento e busca eficiente de livros por título          |
| Lista Encadeada | Cadastro e consulta de usuários                               |
| Fila (Queue)    | Fila de espera de reservas para livros                        |
| Pilha (Stack)   | Histórico de empréstimos e devoluções                         |
| Dicionário      | Mapeamento rápido de ISBN para Livro e matrícula para Usuário |

---

## 🚀 Como Executar

### Opção 1: Rodando pelo Python

**Pré-requisitos:** Python 3.x instalado

1. Instale as dependências:

   ```bash
   pip install ttkbootstrap
   ```
2. Execute o sistema:

   ```bash
   python interface.py
   ```

### Opção 2: Rodando como Programa .exe (sem Python)

1. Vá até a pasta `dist/` (após gerar o executável com PyInstaller)
2. Garanta que estejam juntos:

   * `interface.exe`
   * `minha_biblioteca.json` (opcional, para manter os dados)
   * Pasta `componentes/` (com todos os arquivos .py das abas/telas)
3. Execute `interface.exe` (pode ser levado para qualquer computador Windows!)

---

## 📁 Estrutura de Pastas

    ```text
    Sistema-Biblioteca/
    │
    ├── componentes/
    │   ├── __pycache__/
    │   ├── aba_emprestimos.py
    │   ├── aba_historico.py
    │   ├── aba_livros.py
    │   ├── aba_usuarios.py
    │   ├── login.py
    │
    ├── dist/
    │   └── (arquivos gerados pelo PyInstaller, ex: interface.exe)
    │
    ├── data/
    │   └── minha_biblioteca.json         # Dados persistentes do sistema
    │
    ├── docs/
    │   └── README.md                     # Documentação do projeto
    │
    ├── main.py                           # Ponto de entrada alternativo
    ├── interface.py                      # Ponto de entrada principal/interface gráfica
    ├── arvore_binaria_busca.py           # Implementação da ABB
    ├── lista_encadeada.py                # Implementação da lista encadeada
    ├── estruturas_elementares.py         # Outras estruturas de dados auxiliares
    ├── sistema_biblioteca.py             # Módulo principal do sistema (lógica central)
    ├── interface.spec                    # Arquivo de configuração do PyInstaller
    ├── biblioteca.ico                    # Ícone do sistema
    └── .gitignore                        # Ignorar arquivos não necessários no controle de versão
    ```
---

## 🔐 Permissões

* **Funcionários:** Cadastro, edição e exclusão de livros/usuários, limpeza de histórico.
* **Clientes:** Apenas consultas e solicitações de empréstimo/devolução.
* **Login obrigatório:** Por matrícula e senha.

---

## 💾 Persistência de Dados

Todos os cadastros, histórico e filas são salvos em um arquivo JSON (`minha_biblioteca.json`) no mesmo diretório do executável.

O sistema carrega automaticamente o estado ao iniciar.

---

## 🎨 Personalização

* Ícone próprio do sistema (`biblioteca.ico`) incluído no .exe e na janela da aplicação.
* Visual dark mode com cores neutras, botões destacados e experiência amigável para o usuário.

---

## 🤝 Contribuição

Sinta-se livre para adaptar, melhorar ou sugerir novas funcionalidades!
Ideal para uso em disciplinas de Estrutura de Dados, POO ou como base para sistemas maiores.

---

## 📝 Requisitos Atendidos

- ✔ Cadastro de livros (ABB, título como chave)
- ✔ Cadastro de usuários (Lista Encadeada)
- ✔ Empréstimo de livros (fila de espera por livro)
- ✔ Devolução de livros (histórico/pilha, fila automática)
- ✔ Consultas: por título (ABB) e matrícula (lista encadeada)
- ✔ Interface gráfica e login seguro
- ✔ Geração de .exe (distribuição sem Python)

---
