    -- Criar banco de dados
    CREATE DATABASE IF NOT EXISTS haber_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

    USE haber_db;

    -- Criar usuário com acesso de qualquer máquina na rede
    CREATE USER 'haber_admin'@'%' IDENTIFIED BY 'haber123';

    -- Dar todas as permissões ao usuário no banco haber_db
    GRANT ALL PRIVILEGES ON haber_db.* TO 'haber_admin'@'%';

    -- Aplicar as permissões
    FLUSH PRIVILEGES;

    -- Criar tabela de usuários
    CREATE TABLE IF NOT EXISTS users (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    -- Criar tabela de doenças
    CREATE TABLE IF NOT EXISTS diseases (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100) NOT NULL,
        scientific_name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL,
        treatment TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    -- Criar tabela de precauções para doenças
    CREATE TABLE IF NOT EXISTS disease_precautions (
        id INT PRIMARY KEY AUTO_INCREMENT,
        disease_id INT NOT NULL,
        precaution TEXT NOT NULL,
        FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    -- Criar tabela de análises
    CREATE TABLE IF NOT EXISTS scans (
        id INT PRIMARY KEY AUTO_INCREMENT,
        user_id INT NOT NULL,
        image_path VARCHAR(255) NOT NULL,
        disease_id INT NOT NULL,
        confidence DECIMAL(5,2) NOT NULL,
        latitude DECIMAL(10,8) NULL,
        longitude DECIMAL(11,8) NULL,
        location_source VARCHAR(50) NULL,
        city_name VARCHAR(100) NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

    -- Criar índices para otimização
    CREATE INDEX idx_scans_user ON scans(user_id);
    CREATE INDEX idx_scans_disease ON scans(disease_id);
    CREATE INDEX idx_scans_location ON scans(latitude, longitude);
    CREATE INDEX idx_scans_date ON scans(created_at);

    -- Inserir doenças pré-cadastradas
    INSERT INTO diseases (name, scientific_name, description, treatment) VALUES
    ('Mossaic Virus', 'Vírus do Mosaico', 'Causa manchas amareladas irregulares nas folhas (efeito mosaico), levando à queda da produtividade.', 'Não há tratamento químico direto contra vírus.'),
    ('Southern Blight', 'Sclerotium rolfsii', 'Apodrecimento na base da planta com presença de micélio branco e escleródios.', 'Fungicidas à base de Fluazinam, Thiabendazole ou Azoxystrobina.'),
    ('Sudden Death Syndrome', 'Fusarium virguliforme', 'Clorose entre nervuras e necrose das folhas. Raízes afetadas.', 'Tratamento de sementes com Fluopyram ou Ilevo® (fluopyram + metalaxil).'),
    ('Yellow Mosaic', 'Vírus do Mosaico Amarelo da Soja', 'Amarelecimento das folhas com padrão em mosaico, transmitido por mosca-branca.', 'Controle com Acetamiprido, Bifentrina ou Imidacloprido.'),
    ('Bacterial Blight', 'Pseudomonas savastanoi pv. glycinea', 'Manchas angulares nas folhas com aparência oleosa, evoluindo para necrose.', 'Sem controle curativo direto. Cúpricos podem ser usados preventivamente.'),
    ('Brown Spot', 'Septoria glycines', 'Pequenas manchas marrons nas folhas, que coalescem em lesões maiores.', 'Trifloxistrobina, Azoxystrobina, Picoxystrobina.'),
    ('Crestamento', 'Cercospora kikuchii', 'Manchas avermelhadas nas folhas e vagens, podendo afetar sementes.', 'Mancozebe, Tebuconazol, Fluxapiroxade.'),
    ('Ferrugem', 'Phakopsora pachyrhizi', 'Manchas marrons e ferruginosas com esporulação abundante. Altamente severa.', 'Triazóis (Tebuconazol), Estrobilurinas (Azoxystrobina), Carboxamidas (Fluxapiroxade).'),
    ('Powdery Mildew', 'Microsphaera diffusa', 'Pó branco nas folhas, reduzindo a fotossíntese e produtividade.', 'Enxofre, Protioconazol, Azoxystrobina.'),
    ('Septoria', 'Septoria sojae', 'Lesões circulares e escurecidas nas folhas, similares ao brown spot.', 'Clorotalonil, Mancozebe, Trifloxistrobina.');

    -- Inserir precauções para cada doença
    INSERT INTO disease_precautions (disease_id, precaution) VALUES
    (1, 'Uso de sementes certificadas e livres do vírus'),
    (1, 'Controle de vetores como pulgões (ex: Imidacloprido)'),
    (1, 'Eliminar plantas daninhas hospedeiras'),
    (2, 'Rotação de culturas'),
    (2, 'Boa drenagem do solo'),
    (2, 'Evitar plantio direto sobre palhada contaminada'),
    (3, 'Rotação de culturas'),
    (3, 'Cultivares resistentes'),
    (3, 'Evitar solos compactados e excesso de umidade'),
    (4, 'Controle do vetor'),
    (4, 'Plantio de variedades tolerantes'),
    (4, 'Eliminação de plantas voluntárias'),
    (5, 'Evitar sementes infectadas'),
    (5, 'Rotação de culturas'),
    (5, 'Evitar irrigação por aspersão'),
    (6, 'Tratamento de sementes'),
    (6, 'Aplicação preventiva de fungicidas'),
    (6, 'Monitoramento no início do ciclo'),
    (7, 'Uso de sementes tratadas'),
    (7, 'Rotação de culturas'),
    (7, 'Pulverizações entre R1 e R3'),
    (8, 'Aplicações preventivas baseadas em alertas'),
    (8, 'Cultivares precoces'),
    (8, 'Eliminar sojas voluntárias no vazio sanitário'),
    (9, 'Aplicações preventivas em clima seco'),
    (9, 'Evitar superpopulação de plantas'),
    (10, 'Monitoramento na fase vegetativa'),
    (10, 'Controle químico preventivo'),
    (10, 'Rotação de culturas'); 