# Requisitos Funcionais — Biblioteca Escolar

| ID | Requisito funcional | Critério de aceite |
|---|---|---|
| RF01 | O sistema deve autenticar usuários por e-mail e senha. | Credenciais válidas abrem o dashboard; inválidas exibem erro. |
| RF02 | O sistema deve permitir cadastrar livros. | Livro com dados válidos é persistido. |
| RF03 | O sistema deve listar e pesquisar livros. | Pesquisa filtra por título, autor ou categoria. |
| RF04 | O sistema deve permitir editar livros. | Alterações válidas são salvas. |
| RF05 | O sistema deve permitir excluir livros sem empréstimos vinculados. | Exclusão é realizada apenas quando não há histórico. |
| RF06 | O sistema deve registrar empréstimos. | Empréstimo válido é registrado com usuário, livro e datas. |
| RF07 | O sistema deve impedir empréstimo sem estoque. | Operação é bloqueada quando quantidade disponível é zero. |
| RF08 | O sistema deve registrar devoluções. | Empréstimo passa para devolvido e estoque aumenta. |
| RF09 | O sistema deve exibir histórico de empréstimos. | Lista apresenta usuário, livro, datas e situação. |
| RF10 | O sistema deve exibir indicadores no dashboard. | Mostra total de livros, empréstimos ativos e usuários. |
| RF11 | O sistema deve gerar relatório de livros mais emprestados. | Lista livros ordenados pelo número de empréstimos. |
| RF12 | O sistema deve listar empréstimos em atraso. | Exibe empréstimos ativos com data prevista anterior à data atual. |

## Regras de negócio
- RN01: somente usuário autenticado acessa as áreas internas.
- RN02: quantidade disponível não pode ser negativa.
- RN03: um empréstimo reduz o estoque disponível em uma unidade.
- RN04: uma devolução aumenta o estoque disponível em uma unidade.
- RN05: cada empréstimo pertence a um usuário e a um livro.
- RN06: o sistema não permite excluir livros que possuam histórico de empréstimos.
- RN07: a data prevista para devolução não pode ser anterior à data do empréstimo.
