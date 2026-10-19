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
    codigo TEXT PRIMARY KEY,
    cor TEXT NOT NULL,
    tamanho TEXT,
    material TEXT,
    detalhes TEXT,
    foto TEXT,
    status INTEGER NOT NULL DEFAULT 1,
    data_cadastro TIMESTAMP NOT NULL,
    data_devolucao TIMESTAMP,
    onde_encontrado TEXT,
    categoria_codigo VARCHAR(4) NOT NULL,
    instituicao_cnpj TEXT NOT NULL,
    onde_guardado_codigo TEXT,
    quem_encontrou_username TEXT,
    dono_username TEXT,
    CONSTRAINT fk_categoria 
        FOREIGN KEY (categoria_codigo) 
        REFERENCES categorias (codigo) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    CONSTRAINT fk_instituicao_item 
        FOREIGN KEY (instituicao_cnpj) 
        REFERENCES instituicoes (cnpj) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_onde_guardado 
        FOREIGN KEY (onde_guardado_codigo) 
        REFERENCES salas (codigo) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    CONSTRAINT fk_quem_encontrou 
        FOREIGN KEY (quem_encontrou_username) 
        REFERENCES usuarios (username) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    CONSTRAINT fk_dono 
        FOREIGN KEY (dono_username) 
        REFERENCES usuarios (username) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);

CREATE TABLE contatos (
    codigo VARCHAR(50) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    assunto VARCHAR(100) NOT NULL,
    mensagem TEXT NOT NULL,
    data_envio TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE reivindicacoes (
    -- O protocolo serve como chave primária pois você gera um código único inteiro
    protocolo INT PRIMARY KEY,
    
    -- Relacionamentos (Chaves Estrangeiras)
    autor VARCHAR(100) NOT NULL, -- Supondo que referencia um 'username'
    item_codigo VARCHAR(50) NOT NULL, -- Supondo que o código do item seja texto
    instituicao_cnpj VARCHAR(18) NOT NULL,
    
    -- Campos de texto da Reivindicação
    prova_propriedade TEXT NOT NULL,
    
    -- Controle de Status e Administração
    status VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    observacoes_admin TEXT,
    anexos TEXT, -- Pode guardar links separados por vírgula ou um array JSON
    responsavel_id INT, -- ID do funcionário/admin que atendeu o caso
    
    -- Informações de Devolução
    local_devolucao VARCHAR(255),
    data_devolucao TIMESTAMP,
    
    -- Data de criação
    data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Constraints de integridade referencial (Ajuste os nomes das tabelas se necessário)
    CONSTRAINT fk_reivindicacao_autor FOREIGN KEY (autor) REFERENCES usuarios(username) ON DELETE CASCADE,
    CONSTRAINT fk_reivindicacao_item FOREIGN KEY (item_codigo) REFERENCES itens(codigo) ON DELETE CASCADE,
    CONSTRAINT fk_reivindicacao_instituicao FOREIGN KEY (instituicao_cnpj) REFERENCES instituicoes(cnpj) ON DELETE CASCADE
);

-- CREATE TABLE IF NOT EXISTS itens (
--     id INTEGER PRIMARY KEY,
--     cor TEXT,
--     tamanho TEXT,
--     data TEXT NOT NULL,
--     foto TEXT,
--     categoria_codigo INTEGER NOT NULL,
--     onde_encontrado TEXT NOT NULL,
--     quem_encontrou TEXT NOT NULL,
--     onde_guardado TEXT NOT NULL,
--     CONSTRAINT fk_categoria
--         FOREIGN KEY (categoria_codigo)
--         REFERENCES categorias (codigo)
--         ON DELETE CASCADE
--         ON UPDATE CASCADE
-- );

-- CREATE TABLE IF NOT EXISTS itens (
--     id INTEGER PRIMARY KEY,
--     cor TEXT,
--     tamanho TEXT,
--     data TEXT NOT NULL,
--     foto TEXT,
--     categoria_codigo INTEGER NOT NULL,
--     onde_encontrado TEXT NOT NULL,
--     usuario_matricula TEXT NOT NULL,
--     onde_guardado TEXT NOT NULL,
--     instituicao_cnpj TEXT NOT NULL,

--     CONSTRAINT fk_categoria
--         FOREIGN KEY (categoria_codigo)
--         REFERENCES categorias (codigo)
--         ON DELETE CASCADE
--         ON UPDATE CASCADE,

--     CONSTRAINT fk_usuario
--         FOREIGN KEY (usuario_matricula)
--         REFERENCES usuarios (matricula)
--         ON DELETE CASCADE
--         ON UPDATE CASCADE,

--     CONSTRAINT fk_instituicao
--         FOREIGN KEY (instituicao_cnpj)
--         REFERENCES instituicoes (cnpj)
--         ON DELETE CASCADE
--         ON UPDATE CASCADE

-- );
