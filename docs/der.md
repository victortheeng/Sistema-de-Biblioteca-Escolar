# Diagrama Entidade-Relacionamento (DER)

```mermaid
erDiagram
    USUARIO ||--o{ EMPRESTIMO : realiza
    LIVRO ||--o{ EMPRESTIMO : aparece_em

    USUARIO {
        int id_usuario PK
        string nome
        string email UK
        string senha
        string perfil
    }
    LIVRO {
        int id_livro PK
        string titulo
        string autor
        string categoria
        int quantidade
    }
    EMPRESTIMO {
        int id_emprestimo PK
        date data_emprestimo
        date data_prevista
        date data_devolucao
        int id_usuario FK
        int id_livro FK
        string status
    }
```

## Cardinalidades
- Um usuário pode realizar zero ou vários empréstimos.
- Cada empréstimo pertence a exatamente um usuário.
- Um livro pode aparecer em zero ou vários empréstimos ao longo do tempo.
- Cada empréstimo refere-se a exatamente um livro.

## Observação
`quantidade` representa a quantidade atualmente disponível. O histórico de empréstimos permanece na tabela `Emprestimo`; a devolução altera o status e registra a data efetiva.
