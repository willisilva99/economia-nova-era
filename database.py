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

# Cria a tabela de usuários se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id BIGINT PRIMARY KEY,
    saldo INTEGER DEFAULT 0,
    banco INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,  -- Coluna para XP
    nivel INTEGER DEFAULT 0  -- Coluna para o nível
);
''')
conn.commit()

# Cria a tabela de inventário se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventario (
    user_id BIGINT PRIMARY KEY,
    armas TEXT[] DEFAULT '{}'
);
''')
conn.commit()

# Cria a tabela de investimentos se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS investimentos (
    user_id BIGINT,
    valor INTEGER,
    PRIMARY KEY (user_id, valor)
);
''')
conn.commit()

# Cria a tabela de missões se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS missoes (
    id SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    arma_requerida TEXT,
    recompensa INTEGER NOT NULL
);
''')
conn.commit()

# Cria a tabela de loot se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS loot (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    item TEXT,
    quantidade INTEGER,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
''')
conn.commit()

# Cria a tabela de habilidades se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS habilidades (
    user_id BIGINT PRIMARY KEY,
    combate INTEGER DEFAULT 0,
    coleta INTEGER DEFAULT 0,
    exploracao INTEGER DEFAULT 0
);
''')
conn.commit()

# Funções para obter e atualizar saldo
def get_saldo(user_id):
    cursor.execute("SELECT saldo FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO usuarios (id, saldo, banco, xp, nivel) VALUES (%s, 0, 0, 0, 0)", (user_id,))
        conn.commit()
        return 0
    return result[0]

def update_saldo(user_id, valor):
    saldo_atual = get_saldo(user_id)
    novo_saldo = saldo_atual + valor
    cursor.execute("UPDATE usuarios SET saldo = %s WHERE id = %s", (novo_saldo, user_id))
    conn.commit()
    return novo_saldo

# Funções para obter e atualizar XP e Nível
def adicionar_xp(user_id, valor):
    cursor.execute("UPDATE usuarios SET xp = xp + %s WHERE id = %s", (valor, user_id))
    conn.commit()

def get_xp(user_id):
    cursor.execute("SELECT xp FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Função para obter o valor do banco de um usuário
def get_banco(user_id):
    cursor.execute("SELECT banco FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Função para atualizar o valor do banco de um usuário
def update_banco(user_id, valor):
    cursor.execute("UPDATE usuarios SET banco = banco + %s WHERE id = %s", (valor, user_id))
    conn.commit()

# Função para obter inventário de um usuário
def obter_inventario(user_id):
    cursor.execute("SELECT armas FROM inventario WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else []

# Função para adicionar um item ao inventário de um usuário
def adicionar_item(user_id, item):
    cursor.execute("UPDATE inventario SET armas = array_append(armas, %s) WHERE user_id = %s", (item, user_id))
    conn.commit()

# Fechar a conexão ao banco de dados quando o bot encerrar
def close_connection():
    cursor.close()
    conn.close()
