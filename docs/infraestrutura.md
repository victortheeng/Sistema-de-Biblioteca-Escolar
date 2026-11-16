# Requisitos de Infraestrutura

## Hardware mínimo
- Processador Dual Core ou superior.
- 4 GB de memória RAM.
- 20 GB de armazenamento disponível.
- Monitor e teclado para operação administrativa.

## Software
- Python 3.10 ou superior.
- Flask 3.x (instalado por `requirements.txt`).
- SQLite 3 (incluído no módulo padrão `sqlite3` do Python).
- Navegador atualizado (Chrome, Firefox, Edge ou equivalente).
- Windows, Linux ou macOS.

## Rede
- Acesso à internet para instalação inicial das dependências, se necessário.
- Rede local da escola caso o sistema seja disponibilizado a outros computadores.
- Para implantação em rede, configurar servidor WSGI, firewall e acesso ao banco com política de backup.

## Observação de implantação
A configuração incluída é para desenvolvimento local. O servidor de desenvolvimento do Flask não deve ser usado em produção. Em implantação real, utilizar servidor WSGI, HTTPS, segredo forte, proteção CSRF, backups e controle de acesso.
