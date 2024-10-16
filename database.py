import os
import psycopg2
from urllib.parse import urlparse

# Conectar ao banco de dados PostgreSQL usando a variável de ambiente
url = urlparse(os.getenv("DATABASE_URL"))

conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
cursor = conn.cursor()

# Cria a tabela de usuários se não existir, com o tipo BIGINT para a coluna id
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id BIGINT PRIMARY KEY,
    saldo INTEGER DEFAULT 0,
    banco INTEGER DEFAULT 0
)
''')
conn.commit()

# Função para obter o saldo principal
def get_saldo(user_id):
    cursor.execute("SELECT saldo FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO usuarios (id, saldo, banco) VALUES (%s, 0, 0)", (user_id,))
        conn.commit()
        return 0
    return result[0]

# Função para atualizar o saldo principal
def update_saldo(user_id, valor):
    saldo_atual = get_saldo(user_id)
    novo_saldo = saldo_atual + valor
    cursor.execute("UPDATE usuarios SET saldo = %s WHERE id = %s", (novo_saldo, user_id))
    conn.commit()
    return novo_saldo

# Função para obter o saldo bancário
def get_banco(user_id):
    cursor.execute("SELECT banco FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO usuarios (id, saldo, banco) VALUES (%s, 0, 0)", (user_id,))
        conn.commit()
        return 0
    return result[0]

# Função para atualizar o saldo bancário
def update_banco(user_id, valor):
    banco_atual = get_banco(user_id)
    novo_banco = banco_atual + valor
    cursor.execute("UPDATE usuarios SET banco = %s WHERE id = %s", (novo_banco, user_id))
    conn.commit()
    return novo_banco
