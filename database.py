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

# Comando para alterar o tipo da coluna id para BIGINT
cursor.execute('''
ALTER TABLE usuarios 
ALTER COLUMN id TYPE BIGINT;
''')
conn.commit()

# Cria a tabela de usuários se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id BIGINT PRIMARY KEY,
    saldo INTEGER DEFAULT 0,
    banco INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,  -- Adiciona coluna para XP
    nivel INTEGER DEFAULT 0  -- Adiciona coluna para o nível
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

# Função para obter o saldo principal
def get_saldo(user_id):
    cursor.execute("SELECT saldo FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    if result is None:
        cursor.execute("INSERT INTO usuarios (id, saldo, banco, xp, nivel) VALUES (%s, 0, 0, 0, 0)", (user_id,))
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
        cursor.execute("INSERT INTO usuarios (id, saldo, banco, xp, nivel) VALUES (%s, 0, 0, 0, 0)", (user_id,))
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

# Função para adicionar um item ao inventário
def adicionar_item(user_id, item):
    cursor.execute("SELECT armas FROM inventario WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    
    if result:
        # Adiciona o item ao inventário
        armas = result[0]  # Aqui, armas já é um array se a tabela foi atualizada
        armas.append(item)
        cursor.execute("UPDATE inventario SET armas = %s WHERE user_id = %s", (armas, user_id))
    else:
        # Cria um novo inventário
        cursor.execute("INSERT INTO inventario (user_id, armas) VALUES (%s, %s)", (user_id, [item]))
    conn.commit()

# Função para obter o inventário do usuário
def obter_inventario(user_id):
    cursor.execute("SELECT armas FROM inventario WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else []

# Funções de investimento
def obter_investimentos(user_id):
    cursor.execute("SELECT valor FROM investimentos WHERE user_id = %s", (user_id,))
    result = cursor.fetchall()
    total_investido = sum(investo[0] for investo in result) if result else 0
    return total_investido

def adicionar_investimento(user_id, valor):
    cursor.execute("INSERT INTO investimentos (user_id, valor) VALUES (%s, %s)", (user_id, valor))
    conn.commit()

# Funções de XP e Nível
def adicionar_xp(user_id, valor):
    cursor.execute("UPDATE usuarios SET xp = xp + %s WHERE id = %s", (valor, user_id))
    conn.commit()

def get_xp(user_id):
    cursor.execute("SELECT xp FROM usuarios WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0

# Funções para gerenciar missões
def adicionar_missao(descricao, arma_requerida, recompensa):
    cursor.execute("INSERT INTO missoes (descricao, arma_requerida, recompensa) VALUES (%s, %s, %s)", (descricao, arma_requerida, recompensa))
    conn.commit()

def listar_missoes():
    cursor.execute("SELECT * FROM missoes")
    return cursor.fetchall()

# Funções para gerenciar loot
def adicionar_loot(user_id, item, quantidade):
    cursor.execute("INSERT INTO loot (user_id, item, quantidade) VALUES (%s, %s, %s)", (user_id, item, quantidade))
    conn.commit()

def listar_loot(user_id):
    cursor.execute("SELECT item, quantidade FROM loot WHERE user_id = %s", (user_id,))
    return cursor.fetchall()

# Funções para gerenciar habilidades
def atualizar_habilidades(user_id, combate=None, coleta=None, exploracao=None):
    if combate is not None:
        cursor.execute("UPDATE habilidades SET combate = combate + %s WHERE user_id = %s", (combate, user_id))
    if coleta is not None:
        cursor.execute("UPDATE habilidades SET coleta = coleta + %s WHERE user_id = %s", (coleta, user_id))
    if exploracao is not None:
        cursor.execute("UPDATE habilidades SET exploracao = exploracao + %s WHERE user_id = %s", (exploracao, user_id))
    conn.commit()

def obter_habilidades(user_id):
    cursor.execute("SELECT combate, coleta, exploracao FROM habilidades WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return result if result else (0, 0, 0)  # Retorna 0 para todas as habilidades se não encontrado

# Fechar a conexão ao banco de dados quando o bot encerrar
def close_connection():
    cursor.close()
    conn.close()
