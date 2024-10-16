import sqlite3

# Conecta ao banco de dados (ou cria se não existir)
conn = sqlite3.connect('economia.db')
cursor = conn.cursor()

# Cria a tabela de usuários com saldo e banco, se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY,
    saldo INTEGER DEFAULT 0,
    banco INTEGER DEFAULT 0
)
''')
conn.commit()

# Função para obter o saldo principal
def get_saldo(user_id):
    cursor.execute("SELECT saldo FROM usuarios WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO usuarios (id, saldo, banco) VALUES (?, 0, 0)", (user_id,))
        conn.commit()
        return 0
    return result[0]

# Função para obter o saldo bancário
def get_banco(user_id):
    cursor.execute("SELECT banco FROM usuarios WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO usuarios (id, saldo, banco) VALUES (?, 0, 0)", (user_id,))
        conn.commit()
        return 0
    return result[0]

# Função para atualizar o saldo principal
def update_saldo(user_id, valor):
    saldo_atual = get_saldo(user_id)
    novo_saldo = saldo_atual + valor
    cursor.execute("UPDATE usuarios SET saldo = ? WHERE id = ?", (novo_saldo, user_id))
    conn.commit()
    return novo_saldo

# Função para atualizar o saldo bancário
def update_banco(user_id, valor):
    banco_atual = get_banco(user_id)
    novo_banco = banco_atual + valor
    cursor.execute("UPDATE usuarios SET banco = ? WHERE id = ?", (novo_banco, user_id))
    conn.commit()
    return novo_banco
