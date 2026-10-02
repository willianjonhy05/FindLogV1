CREATE TABLE IF NOT EXISTS instituicoes (
    cnpj TEXT PRIMARY KEY,
    nome TEXT,
    endereco TEXT,
    telefone TEXT,
    email TEXT NOT NULL UNIQUE,
    ativo BOOLEAN DEFAULT FALSE
);