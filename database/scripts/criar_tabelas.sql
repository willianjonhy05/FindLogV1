CREATE TABLE IF NOT EXISTS instituicoes (
    cnpj TEXT PRIMARY KEY,
    nome TEXT,
    endereco TEXT,
    telefone TEXT,
    email TEXT NOT NULL UNIQUE,
    ativo BOOLEAN DEFAULT FALSE
);


CREATE TABLE IF NOT EXISTS salas (
    codigo TEXT PRIMARY KEY,
    telefone TEXT,
    andar TEXT NOT NULL,
    numero TEXT NOT NULL,
    descricao TEXT,
    predio TEXT NOT NULL,
    laboratorio BOOLEAN DEFAULT FALSE,
    sala_de_aula BOOLEAN DEFAULT FALSE,
    instituicao_cnpj TEXT NOT NULL,
    CONSTRAINT fk_instituicao 
        FOREIGN KEY (instituicao_cnpj) 
        REFERENCES instituicoes (cnpj) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);