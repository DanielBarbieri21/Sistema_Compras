"""
Sistema de Compras v2.0 - Arquivo Principal
"""
import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

# Importar e inicializar o banco de dados
import database
database.create_tables()

# Importar a interface principal
from views.main_interface import MainInterface


def main():
    """Função principal da aplicação"""
    try:
        # Criar e executar a aplicação
        app = MainInterface()
        app.run()
        
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()
        
        # Mostrar erro em janela se possível
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Esconder janela principal
            messagebox.showerror("Erro", f"Erro ao iniciar aplicação:\n{e}")
        except:
            pass


if __name__ == "__main__":
    main()

