# -*- coding: utf-8 -*-
"""
Script para popular o banco de dados com dados de teste realistas
Cria um usuário admin e vários scans em diferentes localizações
"""

import mysql.connector
from mysql.connector import Error
from utils.config import get_db_config
from utils.auth import hash_password
from datetime import datetime, timedelta
import random

def populate_database():
    """Popula o banco com dados de teste"""
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("=" * 70)
        print("POPULANDO BANCO DE DADOS COM DADOS DE TESTE")
        print("=" * 70)
        print()

        # ===== CRIAR USUÁRIO ADMIN DE TESTE =====
        print("[1/3] Criando usuario admin de teste...")

        username = "admin"
        password = "admin123"
        name = "Administrador Sistema"
        email = "admin@haber.com"
        hashed_pwd = hash_password(password)

        try:
            cursor.execute("""
                INSERT INTO users (username, name, email, password, role)
                VALUES (%s, %s, %s, %s, 'admin')
            """, (username, name, email, hashed_pwd))
            connection.commit()
            print(f"  [OK] Usuario '{username}' criado com sucesso!")
            print(f"       Login: {username}")
            print(f"       Senha: {password}")
        except Error as e:
            if "Duplicate entry" in str(e):
                print(f"  [AVISO] Usuario '{username}' ja existe, usando existente...")
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_id = cursor.fetchone()[0]
            else:
                raise e

        # Pega o ID do usuário
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            user_id = result[0]
        else:
            print("  [ERRO] Nao foi possivel obter ID do usuario")
            return False

        print(f"  [OK] User ID: {user_id}")
        print()

        # ===== BUSCAR IDs DAS DOENÇAS =====
        print("[2/3] Buscando IDs das doencas...")
        cursor.execute("SELECT id, name FROM diseases")
        diseases = {row[1]: row[0] for row in cursor.fetchall()}
        print(f"  [OK] {len(diseases)} doencas encontradas")
        print()

        # ===== CRIAR SCANS DE TESTE =====
        print("[3/3] Criando scans de teste em diferentes localizacoes...")

        # Localizações realistas no Paraná e região Sul
        locations = [
            # Região Metropolitana de Curitiba
            {"city": "Curitiba", "state": "PR", "lat": -25.4284, "lon": -49.2733},
            {"city": "São José dos Pinhais", "state": "PR", "lat": -25.5347, "lon": -49.2064},
            {"city": "Araucária", "state": "PR", "lat": -25.5934, "lon": -49.4089},
            {"city": "Colombo", "state": "PR", "lat": -25.2919, "lon": -49.2244},
            {"city": "Pinhais", "state": "PR", "lat": -25.4447, "lon": -49.1919},

            # Interior do Paraná
            {"city": "Ponta Grossa", "state": "PR", "lat": -25.0916, "lon": -50.1668},
            {"city": "Londrina", "state": "PR", "lat": -23.3045, "lon": -51.1696},
            {"city": "Maringá", "state": "PR", "lat": -23.4205, "lon": -51.9333},
            {"city": "Cascavel", "state": "PR", "lat": -24.9555, "lon": -53.4552},
            {"city": "Guarapuava", "state": "PR", "lat": -25.3906, "lon": -51.4625},
            {"city": "Foz do Iguaçu", "state": "PR", "lat": -25.5163, "lon": -54.5854},
            {"city": "Toledo", "state": "PR", "lat": -24.7136, "lon": -53.7429},

            # Santa Catarina
            {"city": "Joinville", "state": "SC", "lat": -26.3045, "lon": -48.8487},
            {"city": "Blumenau", "state": "SC", "lat": -26.9194, "lon": -49.0661},
            {"city": "Chapecó", "state": "SC", "lat": -27.0965, "lon": -52.6174},

            # Rio Grande do Sul
            {"city": "Porto Alegre", "state": "RS", "lat": -30.0346, "lon": -51.2177},
            {"city": "Caxias do Sul", "state": "RS", "lat": -29.1634, "lon": -51.1797},
            {"city": "Passo Fundo", "state": "RS", "lat": -28.2624, "lon": -52.4083},
        ]

        # Lista de doenças com probabilidades realistas
        disease_list = [
            "Mossaic Virus",
            "Southern Blight",
            "Sudden Death Syndrome",
            "Yellow Mosaic",
            "Bacterial Blight",
            "Brown Spot",
            "Crestamento",
            "Ferrugem",
            "Powdery Mildew",
            "Septoria"
        ]

        # Criar 50 scans distribuídos ao longo dos últimos 60 dias
        scans_created = 0
        base_date = datetime.now()

        for i in range(50):
            # Seleciona localização aleatória
            location = random.choice(locations)

            # Adiciona variação pequena nas coordenadas (+-0.05 graus, ~5km)
            lat = location['lat'] + random.uniform(-0.05, 0.05)
            lon = location['lon'] + random.uniform(-0.05, 0.05)
            city_name = f"{location['city']}, {location['state']}"

            # Seleciona doença aleatória (Ferrugem mais comum)
            if random.random() < 0.3:
                disease_name = "Ferrugem"  # 30% de chance
            elif random.random() < 0.5:
                disease_name = "Mossaic Virus"  # 20% de chance
            else:
                disease_name = random.choice(disease_list)

            disease_id = diseases.get(disease_name)
            if not disease_id:
                continue

            # Confiança variável (entre 0.75 e 0.99)
            confidence = round(random.uniform(0.75, 0.99), 2)

            # Fontes de localização variadas
            location_sources = ["GPS", "IP", "Manual (Cidade)", "Manual (Mapa)"]
            location_source = random.choice(location_sources)

            # Data aleatória nos últimos 60 dias
            days_ago = random.randint(0, 60)
            hours_ago = random.randint(0, 23)
            minutes_ago = random.randint(0, 59)
            created_at = base_date - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            # Nome de imagem fictício
            image_path = f"folha_soja_{i+1:03d}.jpg"

            # Insere scan
            try:
                cursor.execute("""
                    INSERT INTO scans
                    (user_id, image_path, disease_id, confidence, latitude, longitude,
                     location_source, city_name, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, image_path, disease_id, confidence, lat, lon,
                      location_source, city_name, created_at))
                scans_created += 1
            except Error as e:
                print(f"  [ERRO] Falha ao criar scan {i+1}: {e}")

        connection.commit()
        print(f"  [OK] {scans_created} scans criados com sucesso!")
        print()

        # ===== RESUMO =====
        print("=" * 70)
        print("RESUMO DOS DADOS CRIADOS")
        print("=" * 70)

        # Conta scans por doença
        cursor.execute("""
            SELECT d.name, COUNT(*) as count
            FROM scans s
            JOIN diseases d ON s.disease_id = d.id
            WHERE s.user_id = %s
            GROUP BY d.name
            ORDER BY count DESC
        """, (user_id,))

        print("\nScans por Doenca:")
        print("-" * 70)
        for row in cursor.fetchall():
            print(f"  {row[0]:.<50} {row[1]:>3} scans")

        # Conta scans por cidade
        cursor.execute("""
            SELECT city_name, COUNT(*) as count
            FROM scans
            WHERE user_id = %s
            GROUP BY city_name
            ORDER BY count DESC
            LIMIT 10
        """, (user_id,))

        print("\nTop 10 Cidades com mais Scans:")
        print("-" * 70)
        for row in cursor.fetchall():
            print(f"  {row[0]:.<50} {row[1]:>3} scans")

        # Estatísticas de confiança
        cursor.execute("""
            SELECT
                MIN(confidence) as min_conf,
                AVG(confidence) as avg_conf,
                MAX(confidence) as max_conf
            FROM scans
            WHERE user_id = %s
        """, (user_id,))

        stats = cursor.fetchone()
        print("\nEstatisticas de Confianca:")
        print("-" * 70)
        print(f"  Minima: {float(stats[0]):.2%}")
        print(f"  Media:  {float(stats[1]):.2%}")
        print(f"  Maxima: {float(stats[2]):.2%}")

        print()
        print("=" * 70)
        print("DADOS DE TESTE CRIADOS COM SUCESSO!")
        print("=" * 70)
        print()
        print(f"Login com o usuario admin:")
        print(f"  Usuario: {username}")
        print(f"  Senha: {password}")
        print()
        print("Acesse a pagina de Historico para ver os graficos e o mapa!")
        print("=" * 70)

        return True

    except Error as e:
        print(f"\n[ERRO] Erro ao popular banco de dados: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    populate_database()
