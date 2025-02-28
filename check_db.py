import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM suppliers")
print("Fornecedores no banco:", cursor.fetchall())
conn.close()