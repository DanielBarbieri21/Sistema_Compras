"""
Modelo de Fornecedor para o Sistema de Compras
"""
from typing import Optional, List, Tuple
from database import create_connection


class Supplier:
    """Classe que representa um fornecedor"""
    
    def __init__(self, id: int = None, name: str = "", cnpj: str = "", seller_name: str = ""):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.seller_name = seller_name
    
    def to_dict(self) -> dict:
        """Converte o fornecedor para dicionário"""
        return {
            'id': self.id,
            'name': self.name,
            'cnpj': self.cnpj,
            'seller_name': self.seller_name
        }
    
    @classmethod
    def from_tuple(cls, data: Tuple) -> 'Supplier':
        """Cria um Supplier a partir de uma tupla do banco de dados"""
        return cls(
            id=data[0],
            name=data[1],
            cnpj=data[2],
            seller_name=data[3]
        )
    
    def validate(self) -> List[str]:
        """Valida os dados do fornecedor e retorna lista de erros"""
        errors = []
        
        if not self.name or len(self.name.strip()) < 2:
            errors.append("Nome do fornecedor é obrigatório")
        
        if not self.cnpj or len(self.cnpj.strip()) < 11:
            errors.append("CNPJ é obrigatório")
        
        if not self.seller_name or len(self.seller_name.strip()) < 2:
            errors.append("Nome do vendedor é obrigatório")
        
        return errors
    
    def __str__(self) -> str:
        return f"Supplier({self.id}): {self.name} - {self.cnpj}"
    
    def __repr__(self) -> str:
        return self.__str__()


class SupplierRepository:
    """Repositório para operações de Supplier no banco de dados"""
    
    @staticmethod
    def create(supplier: Supplier) -> Optional[int]:
        """Cria um novo fornecedor no banco de dados"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO suppliers (name, cnpj, seller_name)
                VALUES (?, ?, ?)
            ''', (supplier.name, supplier.cnpj, supplier.seller_name))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Erro ao criar fornecedor: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(supplier_id: int) -> Optional[Supplier]:
        """Busca um fornecedor por ID"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM suppliers WHERE id = ?', (supplier_id,))
            result = cursor.fetchone()
            return Supplier.from_tuple(result) if result else None
        except Exception as e:
            print(f"Erro ao buscar fornecedor {supplier_id}: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all() -> List[Supplier]:
        """Busca todos os fornecedores"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM suppliers ORDER BY name')
            results = cursor.fetchall()
            return [Supplier.from_tuple(result) for result in results]
        except Exception as e:
            print(f"Erro ao buscar todos os fornecedores: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_names() -> List[str]:
        """Retorna apenas os nomes dos fornecedores"""
        suppliers = SupplierRepository.get_all()
        return [supplier.name for supplier in suppliers]
    
    @staticmethod
    def update(supplier: Supplier) -> bool:
        """Atualiza um fornecedor existente"""
        conn = create_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE suppliers
                SET name = ?, cnpj = ?, seller_name = ?
                WHERE id = ?
            ''', (supplier.name, supplier.cnpj, supplier.seller_name, supplier.id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar fornecedor {supplier.id}: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def delete(supplier_id: int) -> bool:
        """Exclui um fornecedor"""
        conn = create_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM suppliers WHERE id = ?', (supplier_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir fornecedor {supplier_id}: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_statistics() -> dict:
        """Retorna estatísticas dos fornecedores"""
        suppliers = SupplierRepository.get_all()
        
        return {
            'total_suppliers': len(suppliers),
            'suppliers': [supplier.to_dict() for supplier in suppliers]
        }

