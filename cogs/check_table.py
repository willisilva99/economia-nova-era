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

# Verifica a estrutura da tabela usuarios
cursor.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'usuarios';")
columns = cursor.fetchall()

for column in columns:
    print(column)

cursor.close()
conn.close()
