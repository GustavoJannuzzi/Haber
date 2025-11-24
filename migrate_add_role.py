# -*- coding: utf-8 -*-
"""
Script de migracao para adicionar a coluna 'role' na tabela users
e definir um usuario como admin
"""

import mysql.connector
from mysql.connector import Error
from utils.config import get_db_config

def run_migration():
    """Executa a migracao para adicionar role aos usuarios"""
    try:
        # Conecta ao banco de dados
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("[OK] Conectado ao banco de dados")

        # Adiciona a coluna role se nao existir
        try:
            cursor.execute("""
                ALTER TABLE users
                ADD COLUMN role VARCHAR(20) DEFAULT 'user'
            """)
            print("[OK] Coluna 'role' adicionada com sucesso")
        except Error as e:
            if "Duplicate column name" in str(e):
                print("[AVISO] Coluna 'role' ja existe")
            else:
                raise e

        # Define o usuario 'joao' como admin
        cursor.execute("""
            UPDATE users
            SET role = 'admin'
            WHERE username = 'joao'
        """)

        if cursor.rowcount > 0:
            print("[OK] Usuario 'joao' definido como admin")
        else:
            print("[AVISO] Usuario 'joao' nao encontrado no banco de dados")

        # Confirma as alteracoes
        connection.commit()
        print("\n[SUCESSO] Migracao concluida com sucesso!")

        # Exibe informacoes dos usuarios
        cursor.execute("SELECT username, name, role FROM users")
        users = cursor.fetchall()

        print("\nUsuarios atualizados:")
        print("-" * 50)
        for user in users:
            username, name, role = user
            role = role if role else 'user'
            print(f"  - {username} ({name}) - Role: {role}")
        print("-" * 50)

    except Error as e:
        print(f"[ERRO] Erro durante a migracao: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("\n[OK] Conexao com o banco de dados encerrada")

    return True

if __name__ == "__main__":
    print("=" * 50)
    print("MIGRACAO: Adicionar coluna 'role' aos usuarios")
    print("=" * 50)
    print()

    run_migration()
