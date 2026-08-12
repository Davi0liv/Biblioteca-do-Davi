"""
Sistema de Gerenciamento de Biblioteca
----------------------------------------
Programa de linha de comando para cadastrar, emprestar, devolver,
listar, buscar e ordenar livros. Os dados sao guardados em um
arquivo de texto (livros.txt) para nao se perderem quando o
programa fecha.
"""

import os

ARQUIVO_LIVROS = "livros.txt"


def carregar_livros(caminho_arquivo):
    """Le o arquivo salvo e devolve a lista de livros.
    Se o arquivo ainda nao existir, devolve uma lista vazia."""
    livros = []
    if os.path.exists(caminho_arquivo):
        arquivo = open(caminho_arquivo, "r", encoding="utf-8")
        for linha in arquivo:
            linha = linha.strip()
            if linha == "":
                continue
            partes = linha.split(";")
            livro = {
                "titulo": partes[0],
                "autor": partes[1],
                "ano": int(partes[2]),
                "isbn": partes[3],
                "status": partes[4],
            }
            livros.append(livro)
        arquivo.close()
    return livros


def salvar_livros(livros, caminho_arquivo):
    """Escreve todos os livros no arquivo, um por linha, separando os dados com ';'."""
    arquivo = open(caminho_arquivo, "w", encoding="utf-8")
    for livro in livros:
        linha = livro["titulo"] + ";" + livro["autor"] + ";" + str(livro["ano"]) + ";" + livro["isbn"] + ";" + livro["status"]
        arquivo.write(linha + "\n")
    arquivo.close()


def cadastrar_livro(livros, titulo, autor, ano, isbn):
    """Cria o dicionario de um livro novo (status inicial 'disponível')
    e adiciona na lista. Devolve o livro criado."""
    novo_livro = {
        "titulo": titulo,
        "autor": autor,
        "ano": ano,
        "isbn": isbn,
        "status": "disponível",
    }
    livros.append(novo_livro)
    return novo_livro


def buscar_livro(livros, termo):
    """Procura, na lista de livros, todos que tenham o termo digitado
    no titulo ou no autor. Nao diferencia maiuscula de minuscula."""
    termo = termo.lower()
    encontrados = []
    for livro in livros:
        if termo in livro["titulo"].lower() or termo in livro["autor"].lower():
            encontrados.append(livro)
    return encontrados


def ordenar_livros(livros, criterio):
    """Ordena a lista de livros comparando vizinhos e trocando de lugar
    quando estao na ordem errada (bubble sort)."""
    tamanho = len(livros)
    for i in range(tamanho):
        for j in range(tamanho - i - 1):
            if livros[j][criterio] > livros[j + 1][criterio]:
                temp = livros[j]
                livros[j] = livros[j + 1]
                livros[j + 1] = temp
    return livros


def listar_livros(livros):
    """Mostra na tela os dados de cada livro da lista recebida."""
    if len(livros) == 0:
        print("Nenhum livro encontrado.")
        return
    for livro in livros:
        print("")
        print("Título: " + livro["titulo"])
        print("Autor: " + livro["autor"])
        print("Ano: " + str(livro["ano"]))
        print("ISBN: " + livro["isbn"])
        print("Status: " + livro["status"])


def main():
    livros = carregar_livros(ARQUIVO_LIVROS)

    if len(livros) == 0:
        # primeira vez rodando o programa: comeca com alguns livros de exemplo
        cadastrar_livro(livros, "Dom Casmurro", "Machado de Assis", 1899, "978-85-359-0277-6")
        cadastrar_livro(livros, "O Cortiço", "Aluísio Azevedo", 1890, "978-85-259-1234-5")
        cadastrar_livro(livros, "Capitães da Areia", "Jorge Amado", 1937, "978-85-01-01234-5")
        salvar_livros(livros, ARQUIVO_LIVROS)

    while True:
        print("")
        print("===== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA =====")
        print("1 - Cadastrar livro")
        print("2 - Emprestar livro")
        print("3 - Devolver livro")
        print("4 - Listar livros")
        print("5 - Buscar livro")
        print("6 - Ordenar listagem")
        print("7 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            ano_texto = input("Ano de publicação: ").strip()
            isbn = input("Código/ISBN: ").strip()

            if not ano_texto.isdigit():
                print("Ano inválido. Cadastro cancelado.")
                continue

            cadastrar_livro(livros, titulo, autor, int(ano_texto), isbn)
            salvar_livros(livros, ARQUIVO_LIVROS)
            print("Livro '" + titulo + "' cadastrado com sucesso!")

        elif opcao == "2":
            termo = input("Título ou autor do livro a emprestar: ").strip()
            encontrados = buscar_livro(livros, termo)

            # procura, entre os encontrados, o primeiro que estiver disponível
            livro_escolhido = None
            for livro in encontrados:
                if livro["status"] == "disponível":
                    livro_escolhido = livro
                    break

            if livro_escolhido:
                livro_escolhido["status"] = "emprestado"
                salvar_livros(livros, ARQUIVO_LIVROS)
                print("Empréstimo registrado: '" + livro_escolhido["titulo"] + "' agora está emprestado.")
            else:
                print("Nenhum livro disponível encontrado com esse termo.")

        elif opcao == "3":
            termo = input("Título ou autor do livro a devolver: ").strip()
            encontrados = buscar_livro(livros, termo)

            # procura, entre os encontrados, o primeiro que estiver emprestado
            livro_escolhido = None
            for livro in encontrados:
                if livro["status"] == "emprestado":
                    livro_escolhido = livro
                    break

            if livro_escolhido:
                livro_escolhido["status"] = "disponível"
                salvar_livros(livros, ARQUIVO_LIVROS)
                print("Devolução registrada: '" + livro_escolhido["titulo"] + "' está disponível novamente.")
            else:
                print("Nenhum livro emprestado encontrado com esse termo.")

        elif opcao == "4":
            listar_livros(livros)

        elif opcao == "5":
            termo = input("Buscar por título ou autor: ").strip()
            listar_livros(buscar_livro(livros, termo))

        elif opcao == "6":
            print("Ordenar por: 1-Título  2-Autor  3-Ano")
            escolha = input("Escolha: ").strip()
            if escolha == "1":
                criterio = "titulo"
            elif escolha == "2":
                criterio = "autor"
            elif escolha == "3":
                criterio = "ano"
            else:
                criterio = None

            if criterio:
                livros = ordenar_livros(livros, criterio)
                listar_livros(livros)
            else:
                print("Opção inválida.")

        elif opcao == "7":
            print("Saindo... até logo!")
            break

        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    main()