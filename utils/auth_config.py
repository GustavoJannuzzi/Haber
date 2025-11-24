import streamlit_authenticator as stauth
import mysql.connector
from mysql.connector import Error
import yaml
from yaml.loader import SafeLoader
from .config import get_db_config
import streamlit as st

# Busca usuários do banco de dados e retorna no formato necessário para o authenticator
def get_users_from_db():
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT username, name, email, password FROM users")
        users = cursor.fetchall()
        
        # Formato necessário para o authenticator
        credentials = {
            "usernames": {}
        }
        
        for user in users:
            credentials["usernames"][user['username']] = {
                'name': user['name'],
                'password': user['password'],
                'email': user['email']
            }
        
        return credentials
        
    except Error as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return None
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Salva novo usuário no banco de dados
def save_users_to_db(username, name, email, password):
    try:
        conn = mysql.connector.connect(**get_db_config())
        cursor = conn.cursor()
        
        # O authenticator já faz o hash da senha
        cursor.execute(
            "INSERT INTO users (username, name, email, password) VALUES (%s, %s, %s, %s)",
            (username, name, email, password)
        )
        conn.commit()
        return True
    except Error as e:
        st.error(f"Erro ao salvar usuário: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Configura e retorna o authenticator
def setup_authenticator():
    config = get_db_config()
    # Garante que port seja int
    if 'port' in config and isinstance(config['port'], str):
        config['port'] = int(config['port'])
    print(f"[DEBUG] Conectando ao MySQL: {config['host']}:{config['port']} (tipo port: {type(config['port'])})")
    conn = mysql.connector.connect(**config)
    credentials = get_users_from_db()
    if not credentials:
        # Logins padrão caso não consiga conectar ao banco
        credentials = {
            "usernames": {
                "joao": {
                    "name": "João Silva",
                    "password": stauth.Hasher(['123456']).generate()[0],
                    "email": "joao.silva@hauber.com"
                },
                "maria": {
                    "name": "Maria Santos",
                    "password": stauth.Hasher(['123456']).generate()[0],
                    "email": "maria.santos@hauber.com"
                }
            }
        }
    
    authenticator = stauth.Authenticate(
        credentials,
        "haber_cookie",  # Nome do cookie
        "haber_key",     # Chave para assinar o cookie
        cookie_expiry_days=30  # Dias até o cookie expirar
    )
    
    return authenticator 