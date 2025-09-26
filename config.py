"""
Configurações do Sistema de Compras
"""
import os
from pathlib import Path

# Diretórios
# Quando empacotado com PyInstaller, __file__ pode apontar para o diretório temporário (_MEIPASS).
# Usamos o diretório do executável para armazenar base de dados, backups e logs.
try:
    import sys
    if getattr(sys, 'frozen', False):
        BASE_DIR = Path(sys.executable).parent
    else:
        BASE_DIR = Path(__file__).parent
except Exception:
    BASE_DIR = Path(__file__).parent
DATABASE_PATH = BASE_DIR / "database.db"
BACKUP_DIR = BASE_DIR / "backups"
LOGS_DIR = BASE_DIR / "logs"

# Criar diretórios se não existirem
BACKUP_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Configurações da aplicação
APP_CONFIG = {
    "title": "Sistema de Compras",
    "version": "2.0.0",
    "geometry": "1400x800",
    "theme": "superhero",  # Tema do ttkbootstrap
    "backup_interval": 24,  # horas
    "max_backups": 30,  # número máximo de backups
}

# Configurações do banco de dados
DATABASE_CONFIG = {
    "path": str(DATABASE_PATH),
    "backup_path": str(BACKUP_DIR),
    "max_connections": 10,
}

# Configurações de validação
VALIDATION_CONFIG = {
    "min_description_length": 3,
    "max_description_length": 200,
    "min_code_length": 1,
    "max_code_length": 50,
    "min_price": 0.01,
    "max_price": 999999.99,
    "min_quantity": 0.01,
    "max_quantity": 999999.99,
}

# Configurações de logging
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": str(LOGS_DIR / "sistema_compras.log"),
    "max_size": 10 * 1024 * 1024,  # 10MB
    "backup_count": 5,
}

