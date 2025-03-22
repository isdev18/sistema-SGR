import sqlite3

conn = sqlite3.connect("sgr.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS avarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    status TEXT
)
""")

# Inserir dados de teste
cursor.execute("INSERT INTO avarias (tipo, descricao, status) VALUES ('Máquina', 'Falha no motor', 'Pendente')")
cursor.execute("INSERT INTO avarias (tipo, descricao, status) VALUES ('Sistema', 'Erro no software', 'Em andamento')")
cursor.execute("INSERT INTO avarias (tipo, descricao, status) VALUES ('Elétrica', 'Curto-circuito', 'Resolvido')")

conn.commit()
conn.close()
print("Banco de dados criado com sucesso!")
