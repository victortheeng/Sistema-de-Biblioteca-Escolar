# Casos de Teste

| ID | Cenário | Procedimento | Resultado esperado |
|---|---|---|---|
| CT01 | Login válido | Informar `ana@escola.com` e `123456`. | Acesso ao dashboard. |
| CT02 | Login inválido | Informar senha incorreta. | Mensagem de credenciais inválidas e permanência no login. |
| CT03 | Cadastro de livro | Preencher todos os campos e quantidade 4. | Livro salvo e exibido na listagem. |
| CT04 | Campo obrigatório | Tentar cadastrar livro sem título. | Cadastro não realizado e mensagem de validação. |
| CT05 | Quantidade negativa | Informar quantidade -1. | Cadastro/edição bloqueado. |
| CT06 | Empréstimo com estoque | Registrar empréstimo de livro com unidades disponíveis. | Empréstimo ativo e quantidade reduzida em 1. |
| CT07 | Empréstimo sem estoque | Tentar emprestar livro com quantidade 0. | Operação bloqueada e estoque permanece 0. |
| CT08 | Devolução | Devolver empréstimo ativo. | Status alterado, data de devolução preenchida e estoque +1. |
| CT09 | Devolução duplicada | Tentar devolver empréstimo já devolvido. | Operação bloqueada, sem alteração no estoque. |
| CT10 | Relatório popularidade | Abrir Relatórios. | Livros aparecem ordenados pelo total de empréstimos. |

## Evidências de execução
Preencha após testar:
- Data:
- Sistema operacional:
- Navegador:
- Responsável:
- Resultado observado por caso:
- Capturas de tela:
