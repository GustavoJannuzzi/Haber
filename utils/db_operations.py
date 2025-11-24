import mysql.connector
from mysql.connector import Error
from datetime import datetime
import streamlit as st
from utils.config import get_db_config

# Estabelece conexão com o banco de dados
def get_db_connection():
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        return connection
    except Error as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Salva uma nova análise no banco de dados  
def save_scan(user_id, image_path, disease_id, confidence, latitude=None, longitude=None, location_source=None, city_name=None):
    conn = get_db_connection()
    if not conn:
        st.error("❌ Falha ao conectar ao banco de dados")
        return False
    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO scans (user_id, image_path, disease_id, confidence, latitude, longitude, location_source, city_name)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (user_id, image_path, disease_id, confidence, latitude, longitude, location_source, city_name)
        cursor.execute(query, values)
        conn.commit()
        return True
    except Error as e:
        st.error(f"❌ Erro ao salvar análise: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém todas as análises de um usuário
def get_user_scans(user_id):
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT s.*, d.name as disease_name, d.scientific_name
        FROM scans s
        JOIN diseases d ON s.disease_id = d.id
        WHERE s.user_id = %s
        ORDER BY s.created_at DESC
        """
        cursor.execute(query, (user_id,))
        return cursor.fetchall()
    except Error as e:
        st.error(f"Erro ao buscar análises: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém uma doença pelo nome
def get_disease_by_name(name):    
    conn = get_db_connection()
    if not conn:
        st.error("❌ Falha ao conectar ao banco de dados")
        return None
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT d.*, GROUP_CONCAT(dp.precaution) as precautions
        FROM diseases d
        LEFT JOIN disease_precautions dp ON d.id = dp.disease_id
        WHERE d.name = %s
        GROUP BY d.id
        """
        cursor.execute(query, (name,))
        result = cursor.fetchone()
        if result:
            if result['precautions']:
                result['precautions'] = result['precautions'].split(',')
            return result
        else:
            st.error(f"❌ Doença não encontrada: {name}")
            return None
    except Error as e:
        st.error(f"❌ Erro ao buscar doença: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém todas as doenças com suas precauções
def get_all_diseases():
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT d.*, GROUP_CONCAT(dp.precaution) as precautions
        FROM diseases d
        LEFT JOIN disease_precautions dp ON d.id = dp.disease_id
        GROUP BY d.id
        """
        cursor.execute(query)
        diseases = cursor.fetchall()
        for disease in diseases:
            if disease['precautions']:
                disease['precautions'] = disease['precautions'].split(',')
            else:
                disease['precautions'] = []
        return diseases
    except Error as e:
        st.error(f"Erro ao buscar doenças: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém estatísticas das análises
def get_scan_statistics():
    conn = get_db_connection()
    if not conn:
        return {}

    try:
        cursor = conn.cursor(dictionary=True)
        stats = {}

        # Total de análises
        cursor.execute("SELECT COUNT(*) as total FROM scans")
        stats['total_scans'] = cursor.fetchone()['total']

        # Análises por doença
        cursor.execute("""
            SELECT d.name, COUNT(*) as count
            FROM scans s
            JOIN diseases d ON s.disease_id = d.id
            GROUP BY d.id
        """)
        stats['disease_counts'] = cursor.fetchall()

        # Análises por região
        cursor.execute("""
            SELECT city_name, COUNT(*) as count
            FROM scans
            WHERE city_name IS NOT NULL
            GROUP BY city_name
        """)
        stats['region_counts'] = cursor.fetchall()

        return stats
    except Error as e:
        st.error(f"Erro ao buscar estatísticas: {e}")
        return {}
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém todos os dados de scans com informações detalhadas para o histórico
def get_all_scans_detailed():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT s.*, d.name as disease_name, d.scientific_name
        FROM scans s
        JOIN diseases d ON s.disease_id = d.id
        ORDER BY s.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        st.error(f"Erro ao buscar análises: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém confiança média por doença
def get_confidence_by_disease():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT d.name as disease_name,
               AVG(s.confidence) as avg_confidence,
               COUNT(*) as count
        FROM scans s
        JOIN diseases d ON s.disease_id = d.id
        GROUP BY d.id, d.name
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        st.error(f"Erro ao buscar confiança média: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Obtém todas as localizações das detecções para mapa
def get_all_scan_locations():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT s.latitude, s.longitude, s.city_name, d.name as disease_name, s.created_at
        FROM scans s
        JOIN diseases d ON s.disease_id = d.id
        WHERE s.latitude IS NOT NULL AND s.longitude IS NOT NULL
        ORDER BY s.created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        st.error(f"Erro ao buscar localizações: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# === Funções para Gestão de Usuários (Admin) ===

# Obtém todos os usuários
def get_all_users():
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT id, username, name, email, created_at, last_login,
               COALESCE(role, 'user') as role
        FROM users
        ORDER BY created_at DESC
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        st.error(f"Erro ao buscar usuários: {e}")
        return []
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Verifica se um usuário é admin
def is_user_admin(user_id):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT COALESCE(role, 'user') as role FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result and result['role'] == 'admin'
    except Error as e:
        st.error(f"Erro ao verificar permissões: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Adiciona um novo usuário
def add_user(username, name, email, password, role='user'):
    from utils.auth import hash_password
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        query = """
        INSERT INTO users (username, name, email, password, role)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (username, name, email, hashed_password, role))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Erro ao adicionar usuário: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Atualiza um usuário existente
def update_user(user_id, name, email, role):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = """
        UPDATE users
        SET name = %s, email = %s, role = %s
        WHERE id = %s
        """
        cursor.execute(query, (name, email, role, user_id))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Erro ao atualizar usuário: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Deleta um usuário
def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Erro ao deletar usuário: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

# Atualiza senha do usuário
def update_user_password(user_id, new_password):
    from utils.auth import hash_password
    conn = get_db_connection()
    if not conn:
        return False

    try:
        cursor = conn.cursor()
        hashed_password = hash_password(new_password)
        query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(query, (hashed_password, user_id))
        conn.commit()
        return True
    except Error as e:
        st.error(f"Erro ao atualizar senha: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close() 