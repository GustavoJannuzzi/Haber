-- Adicionar coluna role na tabela users
USE haber_db;

-- Adicionar a coluna role se ela não existir
ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT 'user';

-- Atualizar um usuário existente para ser admin (substitua 'joao' pelo username desejado)
UPDATE users SET role = 'admin' WHERE username = 'joao';
