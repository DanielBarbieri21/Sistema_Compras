import sqlite3
import json

# Conexão com o banco de dados
def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Criação da tabela de itens
def create_tables():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            code TEXT NOT NULL,
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
def insert_item(description, code, status, suppliers_prices):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO items (description, code, status, suppliers_prices)
        VALUES (?, ?, ?, ?)
    ''', (description, code, status, json.dumps(suppliers_prices)))
    conn.commit()
    conn.close()

# Atualizar item existente
def update_item(item_id, description, code, status, suppliers_prices):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE items
        SET description = ?, code = ?, status = ?, suppliers_prices = ?
        WHERE id = ?
    ''', (description, code, status, json.dumps(suppliers_prices), item_id))
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
    return [(item[0], item[1], item[2], item[3], json.loads(item[4])) for item in items]

# Buscar itens por status
def get_items_by_status(status):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE status = ?', (status,))
    items = cursor.fetchall()
    conn.close()
    return [(item[0], item[1], item[2], item[3], json.loads(item[4])) for item in items]

# Buscar itens por fornecedor
def get_items_by_supplier(supplier):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM items WHERE suppliers_prices LIKE ?', (f'%{supplier}%',))
    items = cursor.fetchall()
    conn.close()
    return [(item[0], item[1], item[2], item[3], json.loads(item[4])) for item in items]

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

# Buscar fornecedores
def get_suppliers():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM suppliers')
    suppliers = cursor.fetchall()
    conn.close()
    return [s[0] for s in suppliers]