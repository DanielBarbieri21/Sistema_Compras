"""
Modelo de Empresa para o Sistema de Compras
"""
from typing import Optional, List, Tuple
from database import create_connection


class Company:
    """Classe que representa uma empresa"""
    
    def __init__(self, id: int = None, name: str = "", cnpj: str = "", buyer_name: str = ""):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.buyer_name = buyer_name
    
    def to_dict(self) -> dict:
        """Converte a empresa para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'cnpj': self.cnpj,
            'buyer_name': self.buyer_name
        }
    
    @classmethod
    def from_tuple(cls, data: Tuple) -> 'Company':
        """Cria uma Company a partir de uma tupla do banco de dados"""
        return cls(
            id=data[0],
            name=data[1],
            cnpj=data[2],
            buyer_name=data[3]
        )
    
    def validate(self) -> List[str]:
        """Valida os dados da empresa e retorna lista de erros"""
        errors = []
        
        if not self.name or len(self.name.strip()) < 2:
            errors.append("Nome da empresa é obrigatório")
        
        if not self.cnpj or len(self.cnpj.strip()) < 11:
            errors.append("CNPJ é obrigatório")
        
        if not self.buyer_name or len(self.buyer_name.strip()) < 2:
            errors.append("Nome do comprador é obrigatório")
        
        return errors
    
    def __str__(self) -> str:
        return f"Company({self.id}): {self.name} - {self.cnpj}"
    
    def __repr__(self) -> str:
        return self.__str__()


class CompanyRepository:
    """Repositório para operações de Company no banco de dados"""
    
    @staticmethod
    def create(company: Company) -> Optional[int]:
        """Cria uma nova empresa no banco de dados"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO company (name, cnpj, buyer_name)
                VALUES (?, ?, ?)
            ''', (company.name, company.cnpj, company.buyer_name))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar empresa: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(company_id: int) -> Optional[Company]:
        """Busca uma empresa por ID"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM company WHERE id = ?', (company_id,))
            result = cursor.fetchone()
            return Company.from_tuple(result) if result else None
        except Exception as e:
            print(f"Erro ao buscar empresa {company_id}: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all() -> List[Company]:
        """Busca todas as empresas"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM company ORDER BY id DESC')
            results = cursor.fetchall()
            return [Company.from_tuple(result) for result in results]
        except Exception as e:
            print(f"Erro ao buscar todas as empresas: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_default() -> Optional[Company]:
        """Busca a empresa padrão (primeira cadastrada)"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM company LIMIT 1')
            result = cursor.fetchone()
            return Company.from_tuple(result) if result else None
        except Exception as e:
            print(f"Erro ao buscar empresa padrão: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def update(company: Company) -> bool:
        """Atualiza uma empresa existente"""
        conn = create_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE company
                SET name = ?, cnpj = ?, buyer_name = ?
                WHERE id = ?
            ''', (company.name, company.cnpj, company.buyer_name, company.id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar empresa {company.id}: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def delete(company_id: int) -> bool:
        """Exclui uma empresa"""
        conn = create_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM company WHERE id = ?', (company_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir empresa {company_id}: {e}")
            return False
        finally:
            conn.close()

