# 🏛️ Sistema de Gerenciamento de Biblioteca 📚

Este projeto implementa um Sistema de Gerenciamento de Biblioteca em Python, aplicando conceitos fundamentais de estruturas de dados. O sistema permite o cadastro de livros e usuários, gerenciamento de empréstimos e devoluções, incluindo filas de espera para livros indisponíveis e um histórico de transações.

## ✨ Funcionalidades Principais

1.  **Cadastro de Livros:**
    * Armazena informações como Título, Autor, ISBN e Quantidade de exemplares.
    * Organizados em uma **Árvore Binária de Busca (ABB)** utilizando o **Título** como chave principal.
    * Cada livro possui sua própria **Fila de Espera** para usuários interessados quando não há exemplares disponíveis.
    * Para buscas eficientes por ISBN, um **mapa (dicionário)** auxiliar é utilizado.

2.  **Cadastro de Usuários:**
    * Registra Nome, Matrícula e Curso do usuário.
    * Armazenados em uma **Lista Encadeada**.

3.  **Empréstimo de Livros:**
    * Verifica a disponibilidade de exemplares.
    * Se disponível, registra o empréstimo e decrementa a quantidade.
    * Caso contrário, o usuário é adicionado à **Fila de Espera** do livro solicitado.

4.  **Devolução de Livros:**
    * Registra a devolução no **Histórico de Empréstimos** (uma **Pilha**).
    * Incrementa a quantidade de exemplares disponíveis.
    * Verifica a **Fila de Espera**: se houver usuários, o livro é automaticamente emprestado ao próximo da fila.

5.  **Consultas:**
    * Busca de livros por **Título** (utilizando a ABB).
    * Busca de livros por **ISBN** (utilizando o mapa auxiliar).
    * Busca de usuários por **Matrícula** (na Lista Encadeada).
    * Visualização do Histórico de Empréstimos.
    * Visualização da Fila de Espera de um livro específico.

## 🛠️ Estruturas de Dados Utilizadas

* **Árvore Binária de Busca (ABB):** Para armazenar e organizar os `Livros` pelo `Título`. Cada nó pode conter uma lista de livros caso haja títulos idênticos com ISBNs diferentes.
* **Dicionário (Hash Map):** Como estrutura auxiliar para mapear `ISBN` a `Livros`, permitindo busca rápida por ISBN.
* **Lista Encadeada:** Para armazenar os `Usuários`.
* **Fila (Queue):** Implementada com `collections.deque`, utilizada para a `Fila de Espera` de cada `Livro`.
* **Pilha (Stack):** Implementada com listas Python, utilizada para manter o `Histórico de Empréstimos`.

## 🚀 Como Executar

1.  **Pré-requisitos:**
    * Python 3.x

2.  **Estrutura dos Arquivos:**
    O projeto está organizado nos seguintes módulos Python:
    * `estruturas_elementares.py`: Define as classes `Livro`, `Usuario`, `Emprestimo`, e as implementações básicas de `Fila` e `Pilha`.
    * `arvore_binaria_busca.py`: Contém a implementação da `NoArvore` e `ArvoreBinariaBusca`.
    * `lista_encadeada.py`: Contém a implementação da `NoLista` e `ListaEncadeada`.
    * `sistema_biblioteca.py`: Contém a classe `SistemaBiblioteca` que integra todas as estruturas e funcionalidades.
    * `main.py`: Ponto de entrada do programa, responsável pelo menu interativo.

3.  **Execução:**
    * Certifique-se de que todos os arquivos `.py` estejam no mesmo diretório.
    * Execute o arquivo principal através do terminal:
        ```bash
        python main.py
        ```
    * Siga as instruções do menu interativo para utilizar o sistema.

## 📝 (Opcional) Persistência de Dados

A funcionalidade de salvar e carregar os dados do sistema em arquivos (ex: JSON, CSV) é uma melhoria opcional que foi implementada para manter o estado do sistema entre execuções.
