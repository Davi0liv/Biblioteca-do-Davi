"""
Sistema de Gerenciamento de Biblioteca
----------------------------------------
Programa de linha de comando para cadastrar, emprestar, devolver,
listar, buscar e ordenar livros. Os dados sao persistidos em um
arquivo CSV (livros.csv) para nao se perderem quando o programa fecha.
"""

import csv
import os

ARQUIVO_LIVROS = "livros.csv"
CAMPOS = ["titulo", "autor", "ano", "isbn", "status"]


def carregar_livros(caminho_arquivo):
    """Le o catalogo salvo em disco e retorna a lista de livros.
    Se o arquivo ainda nao existir (primeira execucao), retorna lista vazia."""
    livros = []
    if os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "r", newline="", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                # todo valor lido de um CSV vem como string, entao convertemos
                # "ano" de volta para numero para permitir ordenacao numerica depois
                linha["ano"] = int(linha["ano"])
                livros.append(linha)
    return livros


def salvar_livros(livros, caminho_arquivo):
    """Escreve a lista de livros inteira no arquivo CSV, sobrescrevendo o conteudo anterior."""
    with open(caminho_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(livros)


def cadastrar_livro(livros, titulo, autor, ano, isbn):
    """Monta o dicionario de um novo livro (status inicial 'disponivel'),
    adiciona na lista em memoria e retorna o dicionario criado."""
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
    """Retorna a lista de livros cujo titulo OU autor contem o termo buscado
    (comparacao sem diferenciar maiusculas/minusculas)."""
    termo = termo.lower()
    return [
        livro for livro in livros
        if termo in livro["titulo"].lower() or termo in livro["autor"].lower()
    ]


def emprestar_livro(livros, termo):
    """Procura, entre os livros encontrados pelo termo, o primeiro que estiver
    'disponível' e muda seu status para 'emprestado'. Retorna o livro alterado
    ou None se nenhum livro disponivel for encontrado."""
    for livro in buscar_livro(livros, termo):
        if livro["status"] == "disponível":
            livro["status"] = "emprestado"
            return livro
    return None


def devolver_livro(livros, termo):
    """Mesma logica do emprestimo, mas ao contrario: procura um livro
    'emprestado' entre os encontrados e devolve o status para 'disponível'."""
    for livro in buscar_livro(livros, termo):
        if livro["status"] == "emprestado":
            livro["status"] = "disponível"
            return livro
    return None


def ordenar_livros(livros, criterio):
    """Retorna uma NOVA lista com os livros ordenados pelo criterio escolhido
    (titulo, autor ou ano). Usa sorted() em vez de .sort() para nao alterar
    a lista original antes de decidirmos usar o resultado."""
    return sorted(livros, key=lambda livro: livro[criterio])


def listar_livros(livros):
    """Imprime os livros formatados em colunas. Nao retorna nada, apenas exibe."""
    if not livros:
        print("\nNenhum livro encontrado.")
        return
    print(f"\n{'TITULO':<30}{'AUTOR':<25}{'ANO':<6}{'ISBN':<18}STATUS")
    print("-" * 95)
    for livro in livros:
        print(f"{livro['titulo']:<30}{livro['autor']:<25}{livro['ano']:<6}{livro['isbn']:<18}{livro['status']}")


def exibir_menu():
    """Apenas imprime as opcoes do menu principal na tela."""
    print("\n===== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA =====")
    print("1 - Cadastrar livro")
    print("2 - Emprestar livro")
    print("3 - Devolver livro")
    print("4 - Listar livros")
    print("5 - Buscar livro")
    print("6 - Ordenar listagem")
    print("7 - Sair")


def main():
    livros = carregar_livros(ARQUIVO_LIVROS)  # recupera o catalogo salvo, se existir

    while True:
        exibir_menu()
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
            salvar_livros(livros, ARQUIVO_LIVROS)  # salva a cada mudança p/ não perder dados
            print(f"Livro '{titulo}' cadastrado com sucesso!")

        elif opcao == "2":
            termo = input("Título ou autor do livro a emprestar: ").strip()
            livro = emprestar_livro(livros, termo)
            if livro:
                salvar_livros(livros, ARQUIVO_LIVROS)
                print(f"Empréstimo registrado: '{livro['titulo']}' agora está emprestado.")
            else:
                print("Nenhum livro disponível encontrado com esse termo.")

        elif opcao == "3":
            termo = input("Título ou autor do livro a devolver: ").strip()
            livro = devolver_livro(livros, termo)
            if livro:
                salvar_livros(livros, ARQUIVO_LIVROS)
                print(f"Devolução registrada: '{livro['titulo']}' está disponível novamente.")
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
            criterio = {"1": "titulo", "2": "autor", "3": "ano"}.get(escolha)
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