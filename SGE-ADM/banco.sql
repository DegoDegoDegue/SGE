CREATE DATABASE IF NOT EXISTS SGE;

USE SGE;

CREATE TABLE IF NOT EXISTS classe (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    ativo VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS marca (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    ativo VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS CA (
    id INT AUTO_INCREMENT PRIMARY KEY,
    descricao VARCHAR(100) NOT NULL,
    CA INT NOT NULL,
    ativo VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS funcionarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100),
    senha VARCHAR(100) NOT NULL,
    data_inclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    marca_id INT,
    CA_id INT,
    classe_id INT NOT NULL,
    data_inclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (marca_id) REFERENCES marca(id),
    FOREIGN KEY (CA_id) REFERENCES CA(id),
    FOREIGN KEY (classe_id) REFERENCES classe(id),
    ativo VARCHAR(1) NOT NULL
);

CREATE TABLE IF NOT EXISTS solicitacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    funcionario_id INT NOT NULL,
    data_solicitacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);

CREATE TABLE IF NOT EXISTS estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT,
    quantidade INT NOT NULL DEFAULT 0,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
);

CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produto_id INT NOT NULL,
    entrada INT DEFAULT 0,
    saida INT DEFAULT 0,
    data_movimentacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tipomov VARCHAR(100),
    solicitacao_id INT,
    funcionario_id INT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id),
    FOREIGN KEY (solicitacao_id) REFERENCES solicitacoes(id),
    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id)
);
 
DELIMITER //

-- Gatilho para adicionar um registro na tabela de estoque quando um novo produto é adicionado
CREATE TRIGGER novo_produto_adicionado AFTER INSERT ON produtos
FOR EACH ROW
BEGIN
    INSERT INTO estoque (produto_id, quantidade) VALUES (NEW.id, 0);
END;
//

-- Gatilho para atualizar a quantidade na tabela de estoque com base nas movimentações de estoque
CREATE TRIGGER atualizar_quantidade_estoque AFTER INSERT ON movimentacoes_estoque
FOR EACH ROW
BEGIN
    DECLARE quantidade_atual INT;

    -- Calcula a quantidade atual no estoque considerando apenas movimentações do funcionário com ID 1
    SELECT COALESCE(SUM(entrada) - SUM(saida), 0) INTO quantidade_atual 
    FROM movimentacoes_estoque 
    WHERE produto_id = NEW.produto_id AND funcionario_id = 1;
    
    -- Atualiza a quantidade no estoque com base na movimentação
    UPDATE estoque 
    SET quantidade = quantidade_atual 
    WHERE produto_id = NEW.produto_id;
END;


//

DELIMITER ;

INSERT INTO funcionarios (nome, senha,ativo) VALUES ('ESTOQUE', '1','S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('ANTONIO FERNANDO LIMA SOARES', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('EDINALDO SOARES DIAS', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('GUSTAVO AZEVEDO BATTISTELLA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('IBANES RAMIRES EPIFANIO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LUCAS DANIEL DE MARCHI', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LUIS EDUARDO GONCALVES', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('MARCOS FELIPE DE MARCHI', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('MARIO LUCIANO DE MARCHI', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('PAULO RHAMOM PEREIRA SOARES', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('RUBSON GONCALVES', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('ALISSON KAYKY ANACLETO DOS', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('BRUNO ANDREY DOS SANTOS', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('BRUNO ROBSON BARBOSA DE', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('CHARLES ALEXANDRE CARDOSO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('CHRISTIAN NOGUEIRA IRINEU', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('CIBELLY PEREIRA MOURA DE ABREU', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('CLOVIS Y CASTRO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('DERLI JUNIOR SANTIAGO PEREIRA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('DHIULLIFER DOS SANTOS DUTRA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('ELITON SANTOS DE MELO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('FELIPE SANTOS DA SILVA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('GIAN ANDRE PILOTTO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('IAN GABRIEL DE ANDRADE', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('IGOR DA ROSA ESPINDOLA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('JOCHUA FORMOSO BUZATTO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LEANDRO CRUZ DA SILVA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LEMUEL FAGUNDES GUIMARAES', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LUCAS VINICIUS SANTOS SOUZA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LUIS FERNANDO DE SOUZA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('LUIS ROGERIO DA SILVA REIS', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('MARCELO ANTONIO DE LIMA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('MATEUS BRITO SOEIRO', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('MATEUS DA SILVA OLIARI', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('PATRICK DOUGLAS DOS SANTOS', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('RICARDO ALEXANDRE DE SOUZA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('SIDINEI ENEZIO VIEIRA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('VINICIUS GOUVEiA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('WELLINGTON MATHEUS PEHL ISRAEL', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('WILLY JEFFERSON PEREIRA', '1', 'S');
INSERT INTO funcionarios (nome, senha, ativo) VALUES ('YURI FERREIRA GOMES', '1', 'S');

INSERT INTO marca (descricao,ativo) VALUES ('GENERICO','S');
INSERT INTO classe (descricao,ativo) VALUES ('EPI','S');

INSERT INTO CA (descricao,CA,ativo) VALUES ('GENERICO','9999999','S');

INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('LUVA TAM 10','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('LUVA TAM 09','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('LUVA TAM 08','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('LUVA TAM 07','1','1','1','S');

INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 38	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 39	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 40	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 41	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 42	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 43	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA VIPOSA TAM 44	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 38	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 39	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 40	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 41	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 42	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 43	','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA KADESH TAM 44	','1','1','1','S');

INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA DE BORRACHA (7 LÉGUAS) TAM 40','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA DE BORRACHA (7 LÉGUAS) TAM 41','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA DE BORRACHA (7 LÉGUAS) TAM 42','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('BOTA DE BORRACHA (7 LÉGUAS) TAM 43','1','1','1','S');

INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('PALMILHA','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('ÓCULOS PROTEÇÃO TRANSPARENTE','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('ÓCULOS PROTEÇÃO PRETO','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('PROTETOR AURICULAR','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('ABAFADOR CONCHA','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('CAPACETE - LARANJA VONDER','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('CAPACETE - BRANCO 3M','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('CARNEIRAS AVULSAS','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('VISEIRA PARA CAPACETE','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('RESPIRADOR FACIAL','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('FILTRO PERFIL RESPIRADOR','1','1','1','S');
INSERT INTO produtos (nome,marca_id,CA_id,classe_id,ativo) VALUES ('MASCARA AZUL DESCARTÁVEL','1','1','1','S');
