# main.py
from sistema_biblioteca import SistemaBiblioteca

def exibir_menu():
    print("\n--- Sistema de Gerenciamento de Biblioteca ---")
    print("1. Cadastrar Livro")
    print("2. Cadastrar Usuário")
    print("3. Realizar Empréstimo de Livro")
    print("4. Realizar Devolução de Livro")
    print("5. Consultar Livro por Título")
    print("6. Consultar Usuário por Matrícula")
    print("7. Exibir Histórico de Empréstimos")
    print("8. Exibir Fila de Espera de um Livro")
    print("9. Listar Todos os Livros (Ordenados por Título)")
    print("10. Listar Todos os Usuários")
    print("0. Sair e Salvar")
    return input("Escolha uma opção: ")

def main():
    sistema = SistemaBiblioteca(arquivo_dados="minha_biblioteca.json") 

    while True:
        opcao = exibir_menu()

        if opcao == '1':
            print("\n--- Cadastro de Livro ---")
            titulo = input("Título: ")
            autor = input("Autor: ")
            isbn = input("ISBN: ")
            while True:
                try:
                    quantidade = int(input("Quantidade de exemplares: "))
                    if quantidade < 0:
                        print("Quantidade não pode ser negativa.")
                    else:
                        break
                except ValueError:
                    print("Entrada inválida para quantidade. Use um número.")
            sistema.cadastrar_livro(titulo, autor, isbn, quantidade)

        elif opcao == '2':
            print("\n--- Cadastro de Usuário ---")
            nome = input("Nome: ")
            matricula = input("Matrícula: ")
            curso = input("Curso: ")
            sistema.cadastrar_usuario(nome, matricula, curso)

        elif opcao == '3':
            print("\n--- Realizar Empréstimo ---")
            matricula = input("Matrícula do usuário: ")
            isbn = input("ISBN do livro: ")
            sistema.realizar_emprestimo(matricula, isbn)

        elif opcao == '4':
            print("\n--- Realizar Devolução ---")
            matricula = input("Matrícula do usuário: ")
            isbn = input("ISBN do livro: ")
            sistema.realizar_devolucao(matricula, isbn)

        elif opcao == '5':
            print("\n--- Consultar Livro por Título ---")

            titulo = input("Título do livro: ")
            sistema.consultar_livro_por_titulo(titulo)

        elif opcao == '6':
            print("\n--- Consultar Usuário por Matrícula ---")
            matricula = input("Matrícula do usuário: ")
            sistema.consultar_usuario_por_matricula(matricula)

        elif opcao == '7':
            sistema.exibir_historico_emprestimos()
            
        elif opcao == '8':
            print("\n--- Exibir Fila de Espera ---")
            isbn = input("ISBN do livro para ver a fila: ")
            sistema.exibir_fila_espera_livro(isbn)

        elif opcao == '9':
            sistema.listar_todos_os_livros()

        elif opcao == '10':
            sistema.listar_todos_os_usuarios()

        elif opcao == '0':
            sistema.salvar_dados() # Salva antes de sair
            print("Saindo do sistema. Até logo! 👋")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()