import discord
from discord.ext import commands
import os

# Configuração do prefixo do bot
bot = commands.Bot(command_prefix="!!")

# Lista de cogs que vamos carregar
cogs = ["trabalho", "investimento", "saldo", "banco"]

# Carregar cada cog
for cog in cogs:
    try:
        bot.load_extension(f"cogs.{cog}")
        print(f"Cog {cog} carregado com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar o cog {cog}: {e}")

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Executar o bot
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
