from passlib.hash import pbkdf2_sha256
import mysql.connector
from mysql.connector import Error
import streamlit as st
from .config import get_db_config

def get_db_connection():
    try:
        connection = mysql.connector.connect(**get_db_config())
        return connection
    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

def verify_password(password, hashed):
    """Verifica se a senha está correta"""
    return pbkdf2_sha256.verify(password, hashed)

def hash_password(password):
    """Cria um hash seguro da senha"""
    return pbkdf2_sha256.hash(password)

def authenticate_user(username, password):
    """Autentica um usuário"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user and verify_password(password, user['password']):
            # Atualiza último login
            cursor.execute("UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = %s", (user['id'],))
            conn.commit()
            return True
        return False
    except Error as e:
        st.error(f"Erro ao autenticar: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def create_user(username, password):
    """Cria um novo usuário"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        return True
    except Error as e:
        st.error(f"Erro ao criar usuário: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Função para migrar usuários existentes
def migrate_existing_users():
    """Migra os usuários do dicionário para o banco de dados"""
    existing_users = {
        "joao": "123456",
        "maria": "senha123"
    }
    
    for username, password in existing_users.items():
        create_user(username, password)

def get_user_id_from_db(username):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        return user['id'] if user else None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def get_user_id():
    return st.session_state.get('user_id', None) 