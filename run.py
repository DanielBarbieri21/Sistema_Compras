"""
Script de inicialização do Sistema de Compras v2.0
"""
import subprocess
import sys
import os
import logging
from pathlib import Path

try:
    from config import LOGS_DIR
    LOGS_DIR_PATH = Path(LOGS_DIR)
except Exception:
    LOGS_DIR_PATH = Path(__file__).parent / "logs"

# Configurar logging para arquivo (útil no executável windowed)
try:
    LOGS_DIR_PATH.mkdir(exist_ok=True)
    logging.basicConfig(
        filename=str(LOGS_DIR_PATH / "startup.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
except Exception:
    # Fallback para logging básico no stdout
    logging.basicConfig(level=logging.INFO)

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
    logging.info("Inicialização do Sistema de Compras iniciada")
    
    # No executável (frozen), não tentar instalar dependências
    is_frozen = getattr(sys, 'frozen', False)
    if not is_frozen:
        # Verificar se as dependências estão instaladas (modo desenvolvimento)
        try:
            import ttkbootstrap
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
        logging.info("Carregando main.main() e iniciando UI")
        from main import main as run_app
        run_app()
        logging.info("Aplicação finalizada")
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicação: {e}")
        logging.exception("Erro ao iniciar aplicação")
        import traceback
        traceback.print_exc()
        # Mostrar diálogo de erro em modo windowed
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Erro", f"Erro ao iniciar aplicação:\n{e}")
        except Exception:
            pass

if __name__ == "__main__":
    main()

