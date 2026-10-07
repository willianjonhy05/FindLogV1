CREATE TABLE IF NOT EXISTS instituicoes (
    cnpj TEXT PRIMARY KEY,
    nome TEXT,
    endereco TEXT,
    telefone TEXT,
    email TEXT NOT NULL UNIQUE,
    ativo BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS categorias (
    codigo VARCHAR(4) PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    descricao TEXT,
    ativa BOOLEAN DEFAULT TRUE
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


CREATE TABLE IF NOT EXISTS usuarios (
    username TEXT PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha TEXT NOT NULL,
    cpf TEXT NOT NULL UNIQUE,
    data_nascimento DATE NOT NULL,
    data_cadastro TIMESTAMP NOT NULL,
    tipo_usuario INTEGER NOT NULL,
    ativo BOOLEAN DEFAULT TRUE,
    foto_perfil TEXT, -- <--- Coluna para salvar o caminho da imagem (opcional)
    instituicao_cnpj TEXT NOT NULL,
    sala_codigo TEXT,
    CONSTRAINT fk_instituicao FOREIGN KEY (instituicao_cnpj) REFERENCES instituicoes (cnpj) ON DELETE CASCADE,
    CONSTRAINT fk_sala FOREIGN KEY (sala_codigo) REFERENCES salas (codigo) ON DELETE SET NULL
);



CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY,
    cor TEXT,
    tamanho TEXT,
    data TEXT NOT NULL,
    foto TEXT,
    categoria_codigo INTEGER NOT NULL,
    onde_encontrado TEXT NOT NULL,
    quem_encontrou TEXT NOT NULL,
    onde_guardado TEXT NOT NULL,
    CONSTRAINT fk_categoria
        FOREIGN KEY (categoria_codigo)
        REFERENCES categorias (codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS itens (
    id INTEGER PRIMARY KEY,
    cor TEXT,
    tamanho TEXT,
    data TEXT NOT NULL,
    foto TEXT,
    categoria_codigo INTEGER NOT NULL,
    onde_encontrado TEXT NOT NULL,
    usuario_matricula TEXT NOT NULL,
    onde_guardado TEXT NOT NULL,
    instituicao_cnpj TEXT NOT NULL,

    CONSTRAINT fk_categoria
        FOREIGN KEY (categoria_codigo)
        REFERENCES categorias (codigo)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_usuario
        FOREIGN KEY (usuario_matricula)
        REFERENCES usuarios (matricula)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT fk_instituicao
        FOREIGN KEY (instituicao_cnpj)
        REFERENCES instituicoes (cnpj)
        ON DELETE CASCADE
        ON UPDATE CASCADE

);
