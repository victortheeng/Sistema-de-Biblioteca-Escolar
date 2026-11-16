PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS Usuario (
  id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
  nome TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  senha TEXT NOT NULL,
  perfil TEXT NOT NULL DEFAULT 'bibliotecario'
);
CREATE TABLE IF NOT EXISTS Livro (
  id_livro INTEGER PRIMARY KEY AUTOINCREMENT,
  titulo TEXT NOT NULL,
  autor TEXT NOT NULL,
  categoria TEXT NOT NULL,
  quantidade INTEGER NOT NULL DEFAULT 0 CHECK(quantidade >= 0)
);
CREATE TABLE IF NOT EXISTS Emprestimo (
  id_emprestimo INTEGER PRIMARY KEY AUTOINCREMENT,
  data_emprestimo TEXT NOT NULL,
  data_devolucao TEXT,
  data_prevista TEXT NOT NULL,
  id_usuario INTEGER NOT NULL,
  id_livro INTEGER NOT NULL,
  status TEXT NOT NULL DEFAULT 'ativo' CHECK(status IN ('ativo','devolvido')),
  FOREIGN KEY(id_usuario) REFERENCES Usuario(id_usuario),
  FOREIGN KEY(id_livro) REFERENCES Livro(id_livro)
);
