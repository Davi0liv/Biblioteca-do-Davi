# Sistema de Gerenciamento de Biblioteca

Sistema em Python, via linha de comando, para controlar o acervo de uma biblioteca: cadastro de livros, empréstimos, devoluções, busca e ordenação. Os dados são salvos em arquivo de texto (`livros.txt`), então o catálogo não se perde quando o programa é fechado e reaberto. Na primeira execução, o programa já cria 3 livros de exemplo pra facilitar os testes.

## Como executar

Requer apenas Python 3 (nenhuma biblioteca externa é necessária):

```
python3 main.py
```

## Principais funcionalidades

- **Cadastrar livro** — título, autor, ano de publicação e código/ISBN (status inicial: "disponível")
- **Emprestar livro** — busca por título/autor e muda o status para "emprestado"
- **Devolver livro** — busca por título/autor e muda o status de volta para "disponível"
- **Listar livros** — exibe todos os livros cadastrados com seus status
- **Buscar livro** — por título ou autor (busca parcial, sem diferenciar maiúsculas/minúsculas)
- **Ordenar listagem** — por título, autor ou ano

## Requisitos técnicos aplicados

| Requisito | Onde está |
|---|---|
| Menu com if/elif/else | Bloco de decisão dentro do `while` em `main()` |
| Estrutura de repetição (while) | Loop principal em `main()`, encerrado com `break` na opção "Sair" |
| Mínimo de 3 funções próprias (parâmetro + retorno) | `carregar_livros`, `cadastrar_livro`, `buscar_livro` e `ordenar_livros` recebem parâmetros e retornam um valor |
| Lista de livros em memória (lista de dicionários) | Variável `livros`, carregada em `main()` |
| Persistência de dados em arquivo | `carregar_livros()` (leitura linha a linha) e `salvar_livros()` (escrita linha a linha), separando os dados de cada livro com `;` |

## Funções do programa

O sistema usa só 6 funções, cada uma fazendo uma coisa só:

- `carregar_livros` / `salvar_livros` — leitura e escrita do arquivo
- `cadastrar_livro` — cria um livro novo
- `buscar_livro` — procura por título/autor (reaproveitada nas opções de emprestar, devolver e buscar)
- `ordenar_livros` — organiza a lista (bubble sort)
- `listar_livros` — exibe os livros na tela

A lógica de emprestar e devolver fica direto dentro do menu (`main()`), reaproveitando `buscar_livro`, em vez de ter uma função própria só pra isso.

## Como a ordenação funciona

`ordenar_livros()` usa o bubble sort (ordenação bolha): percorre a lista comparando dois livros vizinhos por vez e troca os dois de lugar quando estão na ordem errada. Repete esse processo várias vezes até a lista inteira ficar ordenada.

## Estrutura do projeto

```
nome-do-projeto/
├── main.py       # todo o sistema
├── livros.txt    # catálogo salvo (criado automaticamente na primeira execução)
└── README.md
```
