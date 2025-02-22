import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Listar todas as tabelas no banco de dados
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tabelas no banco de dados:", cursor.fetchall())

# Verificar a estrutura da tabela items
cursor.execute("PRAGMA table_info(items)")
print("Colunas da tabela items:", cursor.fetchall())

# Verificar a estrutura da tabela company (opcional, para debugging)
cursor.execute("PRAGMA table_info(company)")
print("Colunas da tabela company:", cursor.fetchall())

# Verificar a estrutura da tabela suppliers (opcional, para debugging)
cursor.execute("PRAGMA table_info(suppliers)")
print("Colunas da tabela suppliers:", cursor.fetchall())

conn.close()