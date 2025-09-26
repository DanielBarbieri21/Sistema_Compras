"""
Modelo de Item para o Sistema de Compras
"""
import json
from typing import Dict, List, Optional, Tuple
from database import create_connection


class Item:
    """Classe que representa um item do sistema de compras"""
    
    def __init__(self, id: int = None, description: str = "", code: str = "", 
                 brand: str = "", status: str = "A Comprar", quantity: float = 0.0, 
                 suppliers_prices: Dict[str, float] = None):
        self.id = id
        self.description = description
        self.code = code
        self.brand = brand or "N/A"
        self.status = status
        self.quantity = float(quantity) if quantity else 0.0
        self.suppliers_prices = suppliers_prices or {}
    
    def to_dict(self) -> Dict:
        """Converte o item para dicionário"""
        return {
            'id': self.id,
            'description': self.description,
            'code': self.code,
            'brand': self.brand,
            'status': self.status,
            'quantity': self.quantity,
            'suppliers_prices': self.suppliers_prices
        }
    
    @classmethod
    def from_tuple(cls, data: Tuple) -> 'Item':
        """Cria um Item a partir de uma tupla do banco de dados"""
        suppliers_prices = json.loads(data[6]) if data[6] else {}
        return cls(
            id=data[0],
            description=data[1],
            code=data[2],
            brand=data[3],
            status=data[4],
            quantity=data[5],
            suppliers_prices=suppliers_prices
        )
    
    def validate(self) -> List[str]:
        """Valida os dados do item e retorna lista de erros"""
        errors = []
        
        if not self.description or len(self.description.strip()) < 3:
            errors.append("Descrição deve ter pelo menos 3 caracteres")
        
        if not self.code or len(self.code.strip()) < 1:
            errors.append("Código é obrigatório")
        
        if self.quantity <= 0:
            errors.append("Quantidade deve ser maior que zero")
        
        if not self.suppliers_prices:
            errors.append("Pelo menos um fornecedor com preço é obrigatório")
        
        for supplier, price in self.suppliers_prices.items():
            if not supplier.strip():
                errors.append("Nome do fornecedor não pode estar vazio")
            if price <= 0:
                errors.append(f"Preço do fornecedor {supplier} deve ser maior que zero")
        
        return errors
    
    def get_total_value(self) -> float:
        """Calcula o valor total do item (quantidade * menor preço)"""
        if not self.suppliers_prices:
            return 0.0
        
        min_price = min(self.suppliers_prices.values())
        return self.quantity * min_price
    
    def get_best_supplier(self) -> Tuple[str, float]:
        """Retorna o fornecedor com menor preço"""
        if not self.suppliers_prices:
            return "", 0.0
        
        best_supplier = min(self.suppliers_prices.items(), key=lambda x: x[1])
        return best_supplier
    
    def __str__(self) -> str:
        return f"Item({self.id}): {self.description} - {self.code} - {self.status}"
    
    def __repr__(self) -> str:
        return self.__str__()


class ItemRepository:
    """Repositório para operações de Item no banco de dados"""
    
    @staticmethod
    def create(item: Item) -> Optional[int]:
        """Cria um novo item no banco de dados"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO items (description, code, brand, status, quantity, suppliers_prices)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                item.description, 
                item.code, 
                item.brand, 
                item.status, 
                item.quantity, 
                json.dumps(item.suppliers_prices)
            ))
            conn.commit()
            item_id = cursor.lastrowid
            return item_id
        except Exception as e:
            print(f"Erro ao criar item: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_by_id(item_id: int) -> Optional[Item]:
        """Busca um item por ID"""
        conn = create_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,))
            result = cursor.fetchone()
            return Item.from_tuple(result) if result else None
        except Exception as e:
            print(f"Erro ao buscar item {item_id}: {e}")
            return None
        finally:
            conn.close()
    
    @staticmethod
    def get_all() -> List[Item]:
        """Busca todos os itens"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items ORDER BY id DESC')
            results = cursor.fetchall()
            return [Item.from_tuple(result) for result in results]
        except Exception as e:
            print(f"Erro ao buscar todos os itens: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_by_status(status: str) -> List[Item]:
        """Busca itens por status"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items WHERE status = ? ORDER BY id DESC', (status,))
            results = cursor.fetchall()
            return [Item.from_tuple(result) for result in results]
        except Exception as e:
            print(f"Erro ao buscar itens por status: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def get_by_supplier(supplier: str) -> List[Item]:
        """Busca itens por fornecedor"""
        conn = create_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM items')
            results = cursor.fetchall()
            items = []
            for result in results:
                item = Item.from_tuple(result)
                if supplier in item.suppliers_prices:
                    items.append(item)
            return items
        except Exception as e:
            print(f"Erro ao buscar itens por fornecedor: {e}")
            return []
        finally:
            conn.close()
    
    @staticmethod
    def update(item: Item) -> bool:
        """Atualiza um item existente"""
        conn = create_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE items
                SET description = ?, code = ?, brand = ?, status = ?, quantity = ?, suppliers_prices = ?
                WHERE id = ?
            ''', (
                item.description, 
                item.code, 
                item.brand, 
                item.status, 
                item.quantity, 
                json.dumps(item.suppliers_prices),
                item.id
            ))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao atualizar item {item.id}: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def delete(item_id: int) -> bool:
        """Exclui um item"""
        conn = create_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Erro ao excluir item {item_id}: {e}")
            return False
        finally:
            conn.close()
    
    @staticmethod
    def get_statistics() -> Dict:
        """Retorna estatísticas dos itens"""
        items = ItemRepository.get_all()
        
        total_items = len(items)
        status_counts = {}
        total_value = 0.0
        
        for item in items:
            status_counts[item.status] = status_counts.get(item.status, 0) + 1
            total_value += item.get_total_value()
        
        return {
            'total_items': total_items,
            'status_counts': status_counts,
            'total_value': total_value,
            'items_to_buy': status_counts.get('A Comprar', 0),
            'items_purchased': status_counts.get('Comprado', 0),
            'items_partial': status_counts.get('Parcialmente Comprado', 0)
        }

