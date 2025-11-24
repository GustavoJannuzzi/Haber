# Teste para verificar se a função de admin funciona

from utils.db_operations import is_user_admin, get_all_users
from utils.auth import get_user_id_from_db

print("=" * 50)
print("TESTE DE VERIFICAÇÃO DE ADMIN")
print("=" * 50)
print()

# Lista todos os usuários
print("Listando todos os usuários:")
users = get_all_users()
for user in users:
    print(f"  ID: {user['id']}, Username: {user['username']}, Nome: {user['name']}, Role: {user['role']}")

print()
print("-" * 50)
print()

# Testa o usuário joao
username = 'joao'
user_id = get_user_id_from_db(username)
print(f"Usuário: {username}")
print(f"ID do usuário: {user_id}")
print(f"É admin? {is_user_admin(user_id)}")

print()

# Testa o usuário maria
username = 'maria'
user_id = get_user_id_from_db(username)
print(f"Usuário: {username}")
print(f"ID do usuário: {user_id}")
print(f"É admin? {is_user_admin(user_id)}")

print()
print("=" * 50)
