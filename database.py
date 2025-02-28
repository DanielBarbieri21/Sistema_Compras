import sqlite3
import json

# Conexão com o banco de dados
def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Criação das tabelas
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            code TEXT NOT NULL,
            brand TEXT,
            status TEXT NOT NULL,
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

# Inserir novo item
def insert_item(description, code, brand, status, suppliers_prices):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (description, code, brand, status, suppliers_prices)
        VALUES (?, ?, ?, ?, ?)
    ''', (description, code, brand, status, json.dumps(suppliers_prices)))
    conn.commit()
    conn.close()

# Atualizar item existente
def update_item(item_id, description, code, brand, status, suppliers_prices):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE items
        SET description = ?, code = ?, brand = ?, status = ?, suppliers_prices = ?
        WHERE id = ?
    ''', (description, code, brand, status, json.dumps(suppliers_prices), item_id))
    conn.commit()
    conn.close()

# Excluir item
def delete_item(item_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# Buscar todos os itens
def get_all_items():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    return [(item[0], item[1], item[2], item[3], item[4], json.loads(item[5])) for item in items]

# Buscar itens por status
def get_items_by_status(status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE status = ?', (status,))
    items = cursor.fetchall()
    conn.close()
    return [(item[0], item[1], item[2], item[3], item[4], json.loads(item[5])) for item in items]

# Buscar itens por fornecedor
def get_items_by_supplier(supplier):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    conn.close()
    result = []
    for item in items:
        suppliers_prices = json.loads(item[5])
        if supplier in suppliers_prices:
            result.append((item[0], item[1], item[2], item[3], item[4], suppliers_prices))
    return result

# Busca combinada por status e fornecedor
def get_items_by_status_and_supplier(status, supplier):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE status = ?', (status,))
    items = cursor.fetchall()
    conn.close()
    result = []
    for item in items:
        suppliers_prices = json.loads(item[5])
        if supplier in suppliers_prices:
            result.append((item[0], item[1], item[2], item[3], item[4], suppliers_prices))
    return result

# Buscar fornecedores
def get_suppliers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM suppliers')
    suppliers = cursor.fetchall()
    conn.close()
    return [s[0] for s in suppliers if s[0]]

# Cadastrar empresa
def insert_company(name, cnpj, buyer_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO company (name, cnpj, buyer_name) VALUES (?, ?, ?)', (name, cnpj, buyer_name))
    conn.commit()
    conn.close()

# Cadastrar fornecedor
def insert_supplier(name, cnpj, seller_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO suppliers (name, cnpj, seller_name) VALUES (?, ?, ?)', (name, cnpj, seller_name))
    conn.commit()
    conn.close()

# Buscar empresa
def get_company():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM company LIMIT 1')
    company = cursor.fetchone()
    conn.close()
    return company

# Atualizar empresa
def update_company(company_id, name, cnpj, buyer_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE company
        SET name = ?, cnpj = ?, buyer_name = ?
        WHERE id = ?
    ''', (name, cnpj, buyer_name, company_id))
    conn.commit()
    conn.close()

# Excluir empresa
def delete_company(company_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM company WHERE id = ?', (company_id,))
    conn.commit()
    conn.close()

# Atualizar fornecedor
def update_supplier(supplier_id, name, cnpj, seller_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE suppliers
        SET name = ?, cnpj = ?, seller_name = ?
        WHERE id = ?
    ''', (name, cnpj, seller_name, supplier_id))
    conn.commit()
    conn.close()

# Excluir fornecedor
def delete_supplier(supplier_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM suppliers WHERE id = ?', (supplier_id,))
    conn.commit()
    conn.close()

# Obter todas as empresas
def get_all_companies():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM company')
    companies = cursor.fetchall()
    conn.close()
    return companies

# Obter todos os fornecedores
def get_all_suppliers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM suppliers')
    suppliers = cursor.fetchall()
    conn.close()
    return suppliers