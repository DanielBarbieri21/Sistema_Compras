"""
Serviço de Backup do Sistema de Compras
"""
import os
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import schedule
import threading
import time

from config import DATABASE_CONFIG, APP_CONFIG


class BackupService:
    """Serviço responsável pelo backup do banco de dados"""
    
    def __init__(self):
        self.backup_dir = Path(DATABASE_CONFIG['backup_path'])
        self.database_path = Path(DATABASE_CONFIG['path'])
        self.max_backups = APP_CONFIG['max_backups']
        self.backup_interval = APP_CONFIG['backup_interval']
        self._scheduler_thread = None
        self._running = False
    
    def create_backup(self, custom_name: str = None) -> Optional[str]:
        """
        Cria um backup do banco de dados
        
        Args:
            custom_name: Nome personalizado para o backup (opcional)
            
        Returns:
            Caminho do arquivo de backup criado ou None se falhou
        """
        try:
            if not self.database_path.exists():
                print("Banco de dados não encontrado para backup")
                return None
            
            # Criar diretório de backup se não existir
            self.backup_dir.mkdir(exist_ok=True)
            
            # Gerar nome do arquivo de backup
            if custom_name:
                backup_filename = f"backup_{custom_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            else:
                backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            
            backup_path = self.backup_dir / backup_filename
            
            # Copiar o arquivo do banco de dados
            shutil.copy2(self.database_path, backup_path)
            
            # Verificar se o backup foi criado corretamente
            if backup_path.exists() and backup_path.stat().st_size > 0:
                print(f"Backup criado com sucesso: {backup_path}")
                self._cleanup_old_backups()
                return str(backup_path)
            else:
                print("Falha ao criar backup - arquivo vazio ou não criado")
                return None
                
        except Exception as e:
            print(f"Erro ao criar backup: {e}")
            return None
    
    def restore_backup(self, backup_path: str) -> bool:
        """
        Restaura um backup do banco de dados
        
        Args:
            backup_path: Caminho do arquivo de backup
            
        Returns:
            True se restaurado com sucesso, False caso contrário
        """
        try:
            backup_file = Path(backup_path)
            
            if not backup_file.exists():
                print(f"Arquivo de backup não encontrado: {backup_path}")
                return False
            
            # Fazer backup do banco atual antes de restaurar
            current_backup = self.create_backup("before_restore")
            if not current_backup:
                print("Não foi possível criar backup do banco atual")
                return False
            
            # Restaurar o backup
            shutil.copy2(backup_file, self.database_path)
            
            # Verificar se a restauração foi bem-sucedida
            if self._verify_database():
                print(f"Backup restaurado com sucesso: {backup_path}")
                return True
            else:
                print("Falha na restauração - banco corrompido")
                # Restaurar o backup anterior
                shutil.copy2(current_backup, self.database_path)
                return False
                
        except Exception as e:
            print(f"Erro ao restaurar backup: {e}")
            return False
    
    def list_backups(self) -> List[dict]:
        """
        Lista todos os backups disponíveis
        
        Returns:
            Lista de dicionários com informações dos backups
        """
        backups = []
        
        try:
            if not self.backup_dir.exists():
                return backups
            
            for backup_file in self.backup_dir.glob("backup_*.db"):
                stat = backup_file.stat()
                backups.append({
                    'filename': backup_file.name,
                    'path': str(backup_file),
                    'size': stat.st_size,
                    'created': datetime.fromtimestamp(stat.st_ctime),
                    'modified': datetime.fromtimestamp(stat.st_mtime)
                })
            
            # Ordenar por data de criação (mais recente primeiro)
            backups.sort(key=lambda x: x['created'], reverse=True)
            
        except Exception as e:
            print(f"Erro ao listar backups: {e}")
        
        return backups
    
    def delete_backup(self, backup_path: str) -> bool:
        """
        Exclui um arquivo de backup
        
        Args:
            backup_path: Caminho do arquivo de backup
            
        Returns:
            True se excluído com sucesso, False caso contrário
        """
        try:
            backup_file = Path(backup_path)
            
            if not backup_file.exists():
                print(f"Arquivo de backup não encontrado: {backup_path}")
                return False
            
            backup_file.unlink()
            print(f"Backup excluído: {backup_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao excluir backup: {e}")
            return False
    
    def _cleanup_old_backups(self):
        """Remove backups antigos mantendo apenas os mais recentes"""
        try:
            backups = self.list_backups()
            
            if len(backups) > self.max_backups:
                # Ordenar por data de criação (mais antigo primeiro)
                backups.sort(key=lambda x: x['created'])
                
                # Excluir backups antigos
                for backup in backups[:-self.max_backups]:
                    self.delete_backup(backup['path'])
                    
        except Exception as e:
            print(f"Erro ao limpar backups antigos: {e}")
    
    def _verify_database(self) -> bool:
        """Verifica se o banco de dados está íntegro"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Verificar se as tabelas principais existem
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = ['items', 'company', 'suppliers']
            if not all(table in tables for table in required_tables):
                return False
            
            # Verificar integridade do banco
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            
            conn.close()
            return result[0] == 'ok'
            
        except Exception as e:
            print(f"Erro ao verificar integridade do banco: {e}")
            return False
    
    def start_automatic_backup(self):
        """Inicia o backup automático"""
        if self._running:
            return
        
        self._running = True
        
        # Agendar backup automático
        schedule.every(self.backup_interval).hours.do(self.create_backup)
        
        # Iniciar thread do scheduler
        self._scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._scheduler_thread.start()
        
        print(f"Backup automático iniciado - intervalo: {self.backup_interval} horas")
    
    def stop_automatic_backup(self):
        """Para o backup automático"""
        self._running = False
        schedule.clear()
        print("Backup automático parado")
    
    def _run_scheduler(self):
        """Executa o scheduler em thread separada"""
        while self._running:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto
    
    def get_backup_info(self) -> dict:
        """Retorna informações sobre o sistema de backup"""
        backups = self.list_backups()
        
        return {
            'backup_dir': str(self.backup_dir),
            'database_path': str(self.database_path),
            'max_backups': self.max_backups,
            'backup_interval': self.backup_interval,
            'total_backups': len(backups),
            'automatic_backup_running': self._running,
            'latest_backup': backups[0] if backups else None
        }

