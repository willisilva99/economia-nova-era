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
    banco INTEGER DEFAULT 0
);
''')
conn.commit()

# Cria a tabela de inventário se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventario (
    user_id BIGINT PRIMARY KEY,
    armas TEXT DEFAULT '[]'
);
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

# Função para adicionar um item ao inventário
def adicionar_item(user_id, item):
    cursor.execute("SELECT armas FROM inventario WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    if result:
        # Adiciona item ao inventário
        armas = eval(result[0])  # Converte de string para lista
        armas.append(item)
        cursor.execute("UPDATE inventario SET armas = %s WHERE user_id = %s", (str(armas), user_id))
    else:
        # Cria um novo inventário
        cursor.execute("INSERT INTO inventario (user_id, armas) VALUES (%s, %s)", (user_id, str([item])))
    conn.commit()

# Função para obter o inventário do usuário
def obter_inventario(user_id):
    cursor.execute("SELECT armas FROM inventario WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    return eval(result[0]) if result else []

# Funções de investimento
def obter_investimentos(user_id):
    # Retorna o total de investimentos para o usuário
    # Aqui você pode implementar uma lógica para armazenar e obter investimentos
    pass

def adicionar_investimento(user_id, valor):
    # Aqui você pode implementar a lógica para adicionar um investimento
    pass

# Fechar a conexão ao banco de dados quando o bot encerrar
def close_connection():
    cursor.close()
    conn.close()
