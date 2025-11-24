# -*- coding: utf-8 -*-
"""
Script para adicionar scans de teste ao usuário João (user_id = 1)
"""

import mysql.connector
from mysql.connector import Error
from utils.config import get_db_config
from datetime import datetime, timedelta
import random

def populate_joao_scans():
    """Adiciona scans de teste ao usuário João"""
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        print("=" * 70)
        print("ADICIONANDO SCANS DE TESTE PARA O USUARIO JOAO (ID=1)")
        print("=" * 70)
        print()

        # Verifica se o usuário João existe
        user_id = 1
        cursor.execute("SELECT id, username, name FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()

        if not user:
            print(f"[ERRO] Usuario com ID {user_id} nao encontrado!")
            return False

        print(f"[OK] Usuario encontrado: {user[1]} ({user[2]})")
        print()

        # ===== BUSCAR IDs DAS DOENÇAS =====
        print("[1/2] Buscando IDs das doencas...")
        cursor.execute("SELECT id, name FROM diseases")
        diseases = {row[1]: row[0] for row in cursor.fetchall()}
        print(f"  [OK] {len(diseases)} doencas encontradas")
        print()

        # ===== CRIAR SCANS DE TESTE =====
        print("[2/2] Criando scans de teste em diferentes localizacoes...")

        # Localizações realistas no Paraná e região Sul
        locations = [
            # Região Metropolitana de Curitiba
            {"city": "Curitiba", "state": "PR", "lat": -25.4284, "lon": -49.2733},
            {"city": "São José dos Pinhais", "state": "PR", "lat": -25.5347, "lon": -49.2064},
            {"city": "Araucária", "state": "PR", "lat": -25.5934, "lon": -49.4089},
            {"city": "Colombo", "state": "PR", "lat": -25.2919, "lon": -49.2244},
            {"city": "Pinhais", "state": "PR", "lat": -25.4447, "lon": -49.1919},
            {"city": "Piraquara", "state": "PR", "lat": -25.4425, "lon": -49.0628},
            {"city": "Almirante Tamandaré", "state": "PR", "lat": -25.3247, "lon": -49.3100},
            {"city": "Campo Largo", "state": "PR", "lat": -25.4595, "lon": -49.5272},

            # Interior do Paraná
            {"city": "Ponta Grossa", "state": "PR", "lat": -25.0916, "lon": -50.1668},
            {"city": "Londrina", "state": "PR", "lat": -23.3045, "lon": -51.1696},
            {"city": "Maringá", "state": "PR", "lat": -23.4205, "lon": -51.9333},
            {"city": "Cascavel", "state": "PR", "lat": -24.9555, "lon": -53.4552},
            {"city": "Guarapuava", "state": "PR", "lat": -25.3906, "lon": -51.4625},
            {"city": "Foz do Iguaçu", "state": "PR", "lat": -25.5163, "lon": -54.5854},
            {"city": "Toledo", "state": "PR", "lat": -24.7136, "lon": -53.7429},
            {"city": "Paranaguá", "state": "PR", "lat": -25.5163, "lon": -48.5095},
            {"city": "Umuarama", "state": "PR", "lat": -23.7661, "lon": -53.3250},
            {"city": "Apucarana", "state": "PR", "lat": -23.5509, "lon": -51.4609},

            # Santa Catarina
            {"city": "Joinville", "state": "SC", "lat": -26.3045, "lon": -48.8487},
            {"city": "Blumenau", "state": "SC", "lat": -26.9194, "lon": -49.0661},
            {"city": "Chapecó", "state": "SC", "lat": -27.0965, "lon": -52.6174},
            {"city": "Florianópolis", "state": "SC", "lat": -27.5954, "lon": -48.5480},
            {"city": "São José", "state": "SC", "lat": -27.6109, "lon": -48.6349},

            # Rio Grande do Sul
            {"city": "Porto Alegre", "state": "RS", "lat": -30.0346, "lon": -51.2177},
            {"city": "Caxias do Sul", "state": "RS", "lat": -29.1634, "lon": -51.1797},
            {"city": "Passo Fundo", "state": "RS", "lat": -28.2624, "lon": -52.4083},
            {"city": "Pelotas", "state": "RS", "lat": -31.7654, "lon": -52.3376},
            {"city": "Santa Maria", "state": "RS", "lat": -29.6868, "lon": -53.8149},
        ]

        # Lista de doenças
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

        # Criar 60 scans distribuídos ao longo dos últimos 90 dias
        scans_created = 0
        base_date = datetime.now()

        for i in range(60):
            # Seleciona localização aleatória
            location = random.choice(locations)

            # Adiciona variação pequena nas coordenadas (+-0.03 graus, ~3km)
            lat = location['lat'] + random.uniform(-0.03, 0.03)
            lon = location['lon'] + random.uniform(-0.03, 0.03)
            city_name = f"{location['city']}, {location['state']}"

            # Seleciona doença aleatória com distribuição realista
            rand = random.random()
            if rand < 0.25:
                disease_name = "Ferrugem"  # 25% de chance (doença mais comum)
            elif rand < 0.45:
                disease_name = "Mossaic Virus"  # 20% de chance
            elif rand < 0.60:
                disease_name = "Brown Spot"  # 15% de chance
            elif rand < 0.73:
                disease_name = "Crestamento"  # 13% de chance
            else:
                disease_name = random.choice(disease_list)

            disease_id = diseases.get(disease_name)
            if not disease_id:
                continue

            # Confiança variável (entre 0.78 e 0.98)
            # Ferrugem tem confiança mais alta (mais fácil de identificar)
            if disease_name == "Ferrugem":
                confidence = round(random.uniform(0.88, 0.98), 2)
            elif disease_name in ["Mossaic Virus", "Yellow Mosaic"]:
                confidence = round(random.uniform(0.85, 0.97), 2)
            else:
                confidence = round(random.uniform(0.78, 0.94), 2)

            # Fontes de localização variadas
            location_sources_weights = [
                ("GPS", 0.40),  # 40% GPS
                ("IP", 0.25),   # 25% IP
                ("Manual (Cidade)", 0.20),  # 20% Manual Cidade
                ("Manual (Mapa)", 0.15)     # 15% Manual Mapa
            ]
            location_source = random.choices(
                [s[0] for s in location_sources_weights],
                weights=[s[1] for s in location_sources_weights]
            )[0]

            # Data aleatória nos últimos 90 dias
            days_ago = random.randint(0, 90)
            hours_ago = random.randint(6, 20)  # Entre 6h e 20h (horário de trabalho)
            minutes_ago = random.randint(0, 59)
            created_at = base_date - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)

            # Nome de imagem fictício
            image_path = f"soja_folha_{i+1:03d}_{disease_name.replace(' ', '_').lower()}.jpg"

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
        print("RESUMO DOS DADOS CRIADOS PARA JOAO")
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
        total_scans = 0
        for row in cursor.fetchall():
            print(f"  {row[0]:.<50} {row[1]:>3} scans")
            total_scans += row[1]
        print(f"  {'TOTAL':.<50} {total_scans:>3} scans")

        # Conta scans por cidade
        cursor.execute("""
            SELECT city_name, COUNT(*) as count
            FROM scans
            WHERE user_id = %s
            GROUP BY city_name
            ORDER BY count DESC
            LIMIT 15
        """, (user_id,))

        print("\nTop 15 Cidades com mais Scans:")
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

        # Distribuição temporal
        cursor.execute("""
            SELECT
                DATE(created_at) as date,
                COUNT(*) as count
            FROM scans
            WHERE user_id = %s
            GROUP BY DATE(created_at)
            ORDER BY count DESC
            LIMIT 5
        """, (user_id,))

        print("\nDias com mais Scans:")
        print("-" * 70)
        for row in cursor.fetchall():
            print(f"  {row[0]}  {row[1]:>3} scans")

        print()
        print("=" * 70)
        print("SCANS ADICIONADOS COM SUCESSO PARA O USUARIO JOAO!")
        print("=" * 70)
        print()
        print("Faca login com:")
        print("  Usuario: joao")
        print("  Senha: 123456")
        print()
        print("Acesse a pagina de Historico para ver os graficos e o mapa!")
        print("=" * 70)

        return True

    except Error as e:
        print(f"\n[ERRO] Erro ao adicionar scans: {e}")
        return False
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    populate_joao_scans()
