import discord
from discord.ext import commands
import os
import random

# Configuração do prefixo do bot
bot = commands.Bot(command_prefix="!!")

# Lista de cogs que vamos carregar
cogs = ["trabalho", "investimento", "saldo", "banco", "loja", "boss", "inventario"]

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

@bot.command(name="status")
async def status(ctx):
    total_users = len(bot.users)  # Número total de usuários
    await ctx.send(f"🤖 **Status do Bot:**\n"
                   f"Estou online e pronto para ajudar!\n"
                   f"Número total de usuários: {total_users}")

@bot.command(name="evento")
async def evento(ctx):
    eventos = [
        "Uma horda de zumbis avança em sua direção! Prepare-se!",
        "Você encontrou um abrigo seguro, mas cuidado com os perigos internos!",
        "Um sobrevivente te pediu ajuda, mas ele pode ser uma armadilha.",
        "Você descobriu um suprimento de comida em uma loja abandonada!",
        "O céu está escurecendo, sinal de uma tempestade. Fique atento!"
    ]
    await ctx.send(random.choice(eventos))

@bot.command(name="ajuda")
async def ajuda(ctx):
    comandos = [
        "!!trabalho - Trabalhe para ganhar moedas.",
        "!!comprar <arma> - Compre uma arma na loja.",
        "!!roubar @membro - Tente roubar moedas de outro jogador.",
        "!!status - Veja o status do bot.",
        "!!evento - Desencadeie um evento aleatório.",
        "!!ajuda - Liste todos os comandos disponíveis.",
        "!!historia - Ouça uma parte da narrativa do apocalipse."
    ]
    await ctx.send("🆘 **Comandos disponíveis:**\n" + "\n".join(comandos))

@bot.command(name="historia")
async def historia(ctx):
    narrativas = [
        "O mundo mudou quando o vírus começou a se espalhar. O que era uma doença comum tornou-se uma ameaça global.",
        "Os sobreviventes se reúnem em comunidades, mas a desconfiança é alta. Cada um luta para se manter vivo.",
        "Rumores falam de um grupo que está tentando encontrar uma cura, mas muitos acreditam que é apenas uma farsa.",
        "Os zumbis não são mais a única ameaça. Outros sobreviventes se tornaram predadores em busca de recursos."
    ]
    await ctx.send(random.choice(narrativas))

# Executar o bot
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
