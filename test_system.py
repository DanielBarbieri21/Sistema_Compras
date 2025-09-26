"""
Teste do Sistema de Compras v2.0
"""
import sys
import io
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa se todas as importações estão funcionando"""
    print("🧪 Testando importações...")
    
    try:
        # Testar configurações
        import config
        print("✅ Config importado com sucesso")
        
        # Testar banco de dados
        import database
        print("✅ Database importado com sucesso")
        
        # Testar modelos
        from models import Item, ItemRepository, Company, CompanyRepository, Supplier, SupplierRepository
        print("✅ Modelos importados com sucesso")
        
        # Testar validadores
        from utils import Validator, CNPJValidator, ItemValidator
        print("✅ Validadores importados com sucesso")
        
        # Testar serviços
        from services import BackupService
        print("✅ Serviços importados com sucesso")
        
        # Testar views
        from views import MainInterface, DashboardView
        print("✅ Views importadas com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def test_database():
    """Testa o banco de dados"""
    print("\n🗄️ Testando banco de dados...")
    
    try:
        import database
        
        # Criar tabelas
        database.create_tables()
        print("✅ Tabelas criadas com sucesso")
        
        # Testar conexão
        conn = database.create_connection()
        if conn:
            print("✅ Conexão com banco estabelecida")
            conn.close()
        else:
            print("❌ Falha na conexão com banco")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no banco de dados: {e}")
        return False

def test_models():
    """Testa os modelos"""
    print("\n📦 Testando modelos...")
    
    try:
        from models import Item, Company, Supplier
        
        # Testar Item
        item = Item(
            description="Item de teste",
            code="TEST001",
            brand="Marca Teste",
            quantity=10.0,
            suppliers_prices={"Fornecedor Teste": 25.50}
        )
        
        errors = item.validate()
        if errors:
            print(f"❌ Erro na validação do item: {errors}")
            return False
        else:
            print("✅ Modelo Item funcionando")
        
        # Testar Company
        company = Company(
            name="Empresa Teste",
            cnpj="11222333000181",  # CNPJ válido
            buyer_name="Comprador Teste"
        )
        
        errors = company.validate()
        if errors:
            print(f"❌ Erro na validação da empresa: {errors}")
            return False
        else:
            print("✅ Modelo Company funcionando")
        
        # Testar Supplier
        supplier = Supplier(
            name="Fornecedor Teste",
            cnpj="11222333000181",  # CNPJ válido
            seller_name="Vendedor Teste"
        )
        
        errors = supplier.validate()
        if errors:
            print(f"❌ Erro na validação do fornecedor: {errors}")
            return False
        else:
            print("✅ Modelo Supplier funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos modelos: {e}")
        return False

def test_validators():
    """Testa os validadores"""
    print("\n🔍 Testando validadores...")
    
    try:
        from utils import CNPJValidator, ItemValidator
        
        # Testar validação de CNPJ
        valid_cnpj = "11222333000181"
        invalid_cnpj = "12345678901234"
        
        if CNPJValidator.validate_cnpj(valid_cnpj):
            print("❌ CNPJ válido foi rejeitado")
            return False
        else:
            print("✅ CNPJ válido aceito")
        
        if not CNPJValidator.validate_cnpj(invalid_cnpj):
            print("❌ CNPJ inválido foi aceito")
            return False
        else:
            print("✅ CNPJ inválido rejeitado")
        
        # Testar validação de item
        errors = ItemValidator.validate_item_data(
            "Item de teste",
            "TEST001",
            "Marca Teste",
            "Fornecedor Teste",
            "25.50",
            "10"
        )
        
        if errors:
            print(f"❌ Item válido foi rejeitado: {errors}")
            return False
        else:
            print("✅ Validação de item funcionando")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos validadores: {e}")
        return False

def test_backup_service():
    """Testa o serviço de backup"""
    print("\n💾 Testando serviço de backup...")
    
    try:
        from services import BackupService
        
        backup_service = BackupService()
        
        # Testar criação de backup
        backup_path = backup_service.create_backup("teste")
        if backup_path:
            print("✅ Backup criado com sucesso")
        else:
            print("❌ Falha ao criar backup")
            return False
        
        # Testar listagem de backups
        backups = backup_service.list_backups()
        print(f"✅ {len(backups)} backups encontrados")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no serviço de backup: {e}")
        return False

def main():
    """Função principal de teste"""
    # Garantir saída em UTF-8 para emojis em consoles Windows
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE COMPRAS v2.0")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_database,
        test_models,
        test_validators,
        test_backup_service
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"📊 RESULTADO: {passed}/{total} testes passaram")
    
    if passed == total:
        print("🎉 Todos os testes passaram! Sistema funcionando corretamente.")
        print("\n🚀 Para iniciar o sistema, execute:")
        print("   python run.py")
    else:
        print("❌ Alguns testes falharam. Verifique os erros acima.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

