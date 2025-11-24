# Teste para verificar dados de confiança

from utils.db_operations import get_confidence_by_disease, get_all_scans_detailed
import pandas as pd

print("=" * 70)
print("TESTE DE DADOS DE CONFIANÇA")
print("=" * 70)
print()

# Busca dados de confiança
confidence_data = get_confidence_by_disease()

print("Dados de confiança por doença:")
print("-" * 70)
for item in confidence_data:
    print(f"Doença: {item['disease_name']}")
    print(f"  Confiança média: {item['avg_confidence']} (tipo: {type(item['avg_confidence'])})")
    print(f"  Contagem: {item['count']} (tipo: {type(item['count'])})")
    print()

print("=" * 70)
print()

# Busca todos os scans
print("Verificando dados brutos dos scans:")
print("-" * 70)
scans = get_all_scans_detailed()
if scans:
    df = pd.DataFrame(scans)
    print(f"Total de scans: {len(scans)}")
    print(f"\nPrimeiros 5 registros:")
    print(df[['disease_name', 'confidence']].head())
    print(f"\nTipos de dados:")
    print(df[['disease_name', 'confidence']].dtypes)
    print(f"\nEstatísticas de confiança:")
    print(df['confidence'].describe())
else:
    print("Nenhum scan encontrado!")

print("=" * 70)
