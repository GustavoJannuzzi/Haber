from utils.db_operations import (
    get_db_connection,
    get_all_diseases,
    get_disease_by_name,
    save_scan,
    get_user_scans,
    get_scan_statistics
)
import traceback

def test_fluxo_completo():
    try:
        print("\n=== INICIANDO TESTE FUNCIONAL DO BANCO DE DADOS ===\n")
        
        # 1. Teste de Conexão
        print("1. Testando conexão com o banco...")
        conn = get_db_connection()
        if not conn:
            print("❌ Falha na conexão com o banco")
            return
        print("✅ Conexão estabelecida com sucesso!")
        conn.close()
        
        # 2. Teste de Doenças
        print("\n2. Testando operações com doenças...")
        diseases = get_all_diseases()
        if not diseases:
            print("❌ Nenhuma doença encontrada no banco")
            return
        print(f"✅ {len(diseases)} doenças encontradas")
        
        # Teste com uma doença específica
        test_disease = diseases[0]['name']
        disease = get_disease_by_name(test_disease)
        if disease:
            print(f"✅ Doença '{test_disease}' encontrada com sucesso")
            print(f"   - Nome científico: {disease['scientific_name']}")
            print(f"   - Precauções: {len(disease['precautions'])} encontradas")
        else:
            print(f"❌ Falha ao buscar doença '{test_disease}'")
        
        # 3. Teste de Scan
        print("\n3. Testando operações de scan...")
        test_scan = {
            'user_id': 1,
            'image_path': 'test_image.jpg',
            'disease_id': disease['id'],
            'confidence': 0.95,
            'latitude': -23.5505,
            'longitude': -46.6333,
            'location_source': 'GPS',
            'city_name': 'São Paulo'
        }
        
        # Salvar scan
        success = save_scan(**test_scan)
        if success:
            print("✅ Scan salvo com sucesso")
        else:
            print("❌ Falha ao salvar scan")
            return
        
        # Buscar scans do usuário
        user_scans = get_user_scans(1)
        if user_scans:
            print(f"✅ {len(user_scans)} scans encontrados para o usuário")
            print(f"   - Último scan: {user_scans[0]['created_at']}")
            print(f"   - Doença: {user_scans[0]['disease_name']}")
            print(f"   - Confiança: {user_scans[0]['confidence']}")
        else:
            print("❌ Nenhum scan encontrado para o usuário")
        
        # 4. Teste de Estatísticas
        print("\n4. Testando estatísticas...")
        stats = get_scan_statistics()
        if stats:
            print(f"✅ Estatísticas obtidas com sucesso")
            print(f"   - Total de análises: {stats['total_scans']}")
            print(f"   - Análises por doença: {len(stats['disease_counts'])}")
            print(f"   - Análises por região: {len(stats['region_counts'])}")
        else:
            print("❌ Falha ao obter estatísticas")
        
        print("\n=== TESTE FUNCIONAL CONCLUÍDO ===\n")
    
    except Exception as e:
        print("\n❌ ERRO NO TESTE:")
        print(f"Tipo do erro: {type(e).__name__}")
        print(f"Mensagem do erro: {str(e)}")
        print("\nStack trace:")
        traceback.print_exc()

# Executar o teste
if __name__ == "__main__":
    test_fluxo_completo() 