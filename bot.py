import discord
from discord.ext import commands
import os
import vip  # Importa as funções de vip.py

# Configurações do bot
intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!!", intents=intents)

# Comando para iniciar o processo de compra de VIP
@bot.command(name="comprarvip")
async def comprar_vip(ctx):
    await vip.comprar_vip(ctx, bot)

# Rodar o bot
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
