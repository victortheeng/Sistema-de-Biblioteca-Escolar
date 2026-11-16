# Biblioteca Escolar

Sistema web para gerenciamento de livros, usuários e empréstimos de uma biblioteca escolar.

## Tecnologias
- Python 3.10+
- Flask
- SQLite
- HTML5, CSS3 e JavaScript

## Funcionalidades
- Login com validação de credenciais e senha armazenada com hash.
- Dashboard com indicadores de livros, empréstimos ativos e usuários.
- Cadastro, pesquisa, edição e exclusão de livros.
- Registro de empréstimos e devoluções.
- Controle automático de unidades disponíveis.
- Histórico de empréstimos.
- Relatório dos livros mais emprestados e empréstimos em atraso.

## Como executar no Windows
Abra o terminal na pasta do projeto e execute:

```bash
py -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
py app.py
```

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Acesso demonstrativo
O banco é criado e populado automaticamente na primeira execução.

- E-mail: `ana@escola.com`
- Senha: `123456`

Também são criados os usuários `carlos@escola.com` e `marina@escola.com`, ambos com a mesma senha demonstrativa.

**Segurança:** as credenciais acima são apenas para demonstração acadêmica. Altere-as antes de qualquer uso real. Defina uma `SECRET_KEY` forte em variável de ambiente e desative `debug` em produção.

## Banco de dados
O SQLite é criado automaticamente em `instance/biblioteca.db`. O script `schema.sql` documenta a estrutura das tabelas. Os dados iniciais incluem 3 usuários, 5 livros e 5 empréstimos de demonstração.

## Estrutura
```text
sistema-biblioteca-escolar/
├── app.py
├── schema.sql
├── requirements.txt
├── README.md
├── docs/
│   ├── requisitos-funcionais.md
│   ├── der.md
│   ├── casos-de-teste.md
│   └── infraestrutura.md
└── app/
    ├── templates/
    └── static/
```

## Observações
- O campo `quantidade` representa unidades atualmente disponíveis para empréstimo.
- Ao registrar empréstimo, a quantidade disponível diminui em uma unidade.
- Ao registrar devolução, a quantidade aumenta em uma unidade.
- Um livro com histórico de empréstimos não pode ser excluído, preservando a integridade referencial.
- Este sistema é uma implementação didática. Para uso real, adicione proteção CSRF, política de senha, controle de permissões, auditoria e configuração de produção.
