"""
Script de inicialização do Sistema de Compras v2.0
"""
import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias"""
    try:
        print("Instalando dependências...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 50)
    print("Sistema de Compras v2.0")
    print("=" * 50)
    
    # Verificar se as dependências estão instaladas
    try:
        import ttkbootstrap
        import matplotlib
        import openpyxl
        import reportlab
        import schedule
        print("✅ Todas as dependências estão instaladas")
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("Instalando dependências automaticamente...")
        
        if not install_requirements():
            print("❌ Falha ao instalar dependências. Instale manualmente:")
            print("pip install -r requirements.txt")
            return
    
    # Iniciar a aplicação
    try:
        print("🚀 Iniciando Sistema de Compras...")
        from main import main as run_app
        run_app()
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

