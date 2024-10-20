import discord
from discord.ext import commands
from discord import Embed
import os
import vip  # Importa as funções de vip.py

# Configurações do bot
intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!!", intents=intents)

# Rodar o bot
TOKEN = os.getenv("TOKEN")  # Certifique-se de definir a variável de ambiente TOKEN
bot.run(TOKEN)
