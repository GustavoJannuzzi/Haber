import streamlit_authenticator as stauth

def generate_user_sql():
    # Dados do usuário
    username = 'teste'
    name = 'Usuário Teste'
    email = 'teste@email.com'
    password = 'teste123'
    
    # Gera o hash da senha
    hashed_password = stauth.Hasher([password]).generate()[0]
    
    # Gera o comando SQL
    sql = f"""
-- Primeiro remove o usuário se ele já existir
DELETE FROM users WHERE username = '{username}';

-- Insere o novo usuário
INSERT INTO users (username, name, email, password) 
VALUES ('{username}', '{name}', '{email}', '{hashed_password}');
"""
    
    print("\n=== Comando SQL para criar usuário ===")
    print(sql)
    print("\n=== Credenciais para teste ===")
    print(f"Username: {username}")
    print(f"Senha: {password}")

if __name__ == "__main__":
    generate_user_sql() 