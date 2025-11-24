import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

def get_db_config():
    """Retorna a configuração do banco de dados"""
    # Força 127.0.0.1 para evitar problemas de DNS
    return {
        'host': '127.0.0.1',
        'user': os.getenv('DB_USER', 'haber_admin'),
        'password': os.getenv('DB_PASSWORD', 'haber123'),
        'database': os.getenv('DB_NAME', 'haber_db'),
        'port': int(os.getenv('DB_PORT', '3306'))
    } 