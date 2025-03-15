import sqlite3
import json

# Função para conectar ao banco de dados
def create_connection():
    try:
        conn = sqlite3.connect('database.db')
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Criação das tabelas
def create_tables():
    conn = create_connection()
    if not conn:
        return
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            code TEXT NOT NULL,
            brand TEXT,
            status TEXT NOT NULL,
            quantity REAL NOT NULL,  -- Ajustado para REAL para suportar float
            suppliers_prices TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS company (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            buyer_name TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            seller_name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Inserir novo item (substitui a função add_item)
def insert_item(description, code, brand, status, quantity, suppliers_prices):
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (description, code, brand, status, quantity, suppliers_prices)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (description, code, brand, status, float(quantity) if quantity else 0.0, json.dumps(suppliers_prices)))
        conn.commit()
        cursor.execute('SELECT last_insert_rowid()')
        item_id = cursor.fetchone()[0]
        print(f"Item inserido com sucesso (ID={item_id}): {description}, {code}")
        return item_id
    except Exception as e:
        print(f"Erro ao inserir item: {e}")
        return None
    finally:
        conn.close()

# Função ajustada para adicionar item (compatível com interface.py)
def add_item(description, code, brand, quantity):
    return insert_item(description, code, brand, "A Comprar", quantity, {})

# Atualizar item existente
def update_item(item_id, description, code, brand, status, quantity, suppliers_prices):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE items
            SET description = ?, code = ?, brand = ?, status = ?, quantity = ?, suppliers_prices = ?
            WHERE id = ?
        ''', (description, code, brand, status, float(quantity) if quantity else 0.0, json.dumps(suppliers_prices), item_id))
        conn.commit()
        print(f"Item {item_id} atualizado com sucesso: {description}, Preços: {suppliers_prices}")
    except Exception as e:
        print(f"Erro ao atualizar item {item_id}: {e}")
    finally:
        conn.close()

# Excluir item
def delete_item(item_id):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
        conn.commit()
        print(f"Item {item_id} excluído com sucesso")
    except Exception as e:
        print(f"Erro ao excluir item: {e}")
    finally:
        conn.close()

# Buscar todos os itens
def get_all_items():
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        return [(item[0], item[1], item[2], item[3], item[4], item[5], json.loads(item[6])) for item in items]
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        return []
    finally:
        conn.close()

# Buscar itens por status
def get_items_by_status(status):
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE status = ?', (status,))
        items = cursor.fetchall()
        return [(item[0], item[1], item[2], item[3], item[4], item[5], json.loads(item[6])) for item in items]
    except Exception as e:
        print(f"Erro ao buscar itens por status: {e}")
        return []
    finally:
        conn.close()

# Buscar itens por fornecedor
def get_items_by_supplier(supplier):
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = cursor.fetchall()
        result = []
        for item in items:
            suppliers_prices = json.loads(item[6])
            if supplier in suppliers_prices:
                result.append((item[0], item[1], item[2], item[3], item[4], item[5], suppliers_prices))
        return result
    except Exception as e:
        print(f"Erro ao buscar itens por fornecedor: {e}")
        return []
    finally:
        conn.close()

# Busca combinada por status e fornecedor
def get_items_by_status_and_supplier(status, supplier):
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items WHERE status = ?', (status,))
        items = cursor.fetchall()
        result = []
        for item in items:
            suppliers_prices = json.loads(item[6])
            if supplier in suppliers_prices:
                result.append((item[0], item[1], item[2], item[3], item[4], item[5], suppliers_prices))
        return result
    except Exception as e:
        print(f"Erro ao buscar itens por status e fornecedor: {e}")
        return []
    finally:
        conn.close()

# Buscar fornecedores (ajustado para buscar a partir de suppliers_prices)
def get_suppliers():
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM suppliers')
        suppliers = cursor.fetchall()
        return [supplier[0] for supplier in suppliers]  # Retorna apenas os nomes dos fornecedores
    except Exception as e:
        print(f"Erro ao buscar fornecedores: {e}")
        return []
    finally:
        conn.close()

# Cadastrar empresa
def insert_company(name, cnpj, buyer_name):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO company (name, cnpj, buyer_name) VALUES (?, ?, ?)', (name, cnpj, buyer_name))
        conn.commit()
        print(f"Empresa cadastrada: {name}")
    except Exception as e:
        print(f"Erro ao cadastrar empresa: {e}")
    finally:
        conn.close()

# Cadastrar fornecedor
def insert_supplier(name, cnpj, seller_name):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO suppliers (name, cnpj, seller_name) VALUES (?, ?, ?)', (name, cnpj, seller_name))
        conn.commit()
        print(f"Fornecedor cadastrado: {name}")
    except Exception as e:
        print(f"Erro ao cadastrar fornecedor: {e}")
    finally:
        conn.close()

# Buscar empresa
def get_company():
    conn = create_connection()
    if not conn:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM company LIMIT 1')
        company = cursor.fetchone()
        return company
    except Exception as e:
        print(f"Erro ao buscar empresa: {e}")
        return None
    finally:
        conn.close()

# Atualizar empresa
def update_company(company_id, name, cnpj, buyer_name):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE company
            SET name = ?, cnpj = ?, buyer_name = ?
            WHERE id = ?
        ''', (name, cnpj, buyer_name, company_id))
        conn.commit()
        print(f"Empresa {company_id} atualizada: {name}")
    except Exception as e:
        print(f"Erro ao atualizar empresa: {e}")
    finally:
        conn.close()

# Excluir empresa
def delete_company(company_id):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM company WHERE id = ?', (company_id,))
        conn.commit()
        print(f"Empresa {company_id} excluída")
    except Exception as e:
        print(f"Erro ao excluir empresa: {e}")
    finally:
        conn.close()

# Atualizar fornecedor
def update_supplier(supplier_id, name, cnpj, seller_name):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE suppliers
            SET name = ?, cnpj = ?, seller_name = ?
            WHERE id = ?
        ''', (name, cnpj, seller_name, supplier_id))
        conn.commit()
        print(f"Fornecedor {supplier_id} atualizado: {name}")
    except Exception as e:
        print(f"Erro ao atualizar fornecedor: {e}")
    finally:
        conn.close()

# Excluir fornecedor
def delete_supplier(supplier_id):
    conn = create_connection()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM suppliers WHERE id = ?', (supplier_id,))
        conn.commit()
        print(f"Fornecedor {supplier_id} excluído")
    except Exception as e:
        print(f"Erro ao excluir fornecedor: {e}")
    finally:
        conn.close()

# Obter todas as empresas
def get_all_companies():
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM company')
        companies = cursor.fetchall()
        return companies
    except Exception as e:
        print(f"Erro ao buscar empresas: {e}")
        return []
    finally:
        conn.close()

# Obter todos os fornecedores (da tabela suppliers)
def get_all_suppliers():
    conn = create_connection()
    if not conn:
        return []
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM suppliers')
        suppliers = cursor.fetchall()
        return suppliers
    except Exception as e:
        print(f"Erro ao buscar fornecedores: {e}")
        return []
    finally:
        conn.close()

# Inicializar o banco de dados ao importar o módulo
create_tables()