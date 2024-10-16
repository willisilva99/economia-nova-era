import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de intents e do prefixo do bot
intents = discord.Intents.default()
intents.members = True  # Ativando intents para acessar informações de membros
bot = commands.Bot(command_prefix="!!", intents=intents)

# Lista de cogs que vamos carregar
cogs = [
    "trabalho",        # Sistema de trabalho
    "investimento",    # Sistema de investimento
    "saldo",           # Sistema de saldo
    "banco",           # Sistema bancário
    "loja",            # Sistema de loja
    "boss",            # Sistema de bosses
    "inventario",      # Sistema de inventário
    "nivel",           # Sistema de níveis e XP
    "missao",          # Sistema de missões diárias
    "pvp"              # Sistema de PvP
]

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
    total_users = len(set(bot.get_all_members()))  # Número total de usuários únicos
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
    comandos = {
        "🛠️ trabalho": "!!trabalho - Trabalhe para ganhar moedas.",
        "🛒 comprar": "!!comprar <arma> - Compre uma arma na loja.",
        "💰 roubar": "!!roubar @membro - Tente roubar moedas de outro jogador.",
        "📊 status": "!!status - Veja o status do bot.",
        "🎲 evento": "!!evento - Desencadeie um evento aleatório.",
        "❓ ajuda": "!!ajuda - Liste todos os comandos disponíveis.",
        "📖 historia": "!!historia - Ouça uma parte da narrativa do apocalipse.",
        "⚔️ listar_armas": "!!listar_armas - Veja a lista de armas disponíveis na loja.",
        "📈 investir": "!!investir <valor> - Invista seu saldo e tenha chance de ganhar ou perder dinheiro.",
        "📊 ver_investimentos": "!!ver_investimentos - Veja o total investido.",
        "🚫 cancelar_investimento": "!!cancelar_investimento - Cancele seu investimento e recupere parte do valor.",
        "👾 ver_bosses": "!!ver_bosses - Veja todos os bosses disponíveis para lutar.",
        "🔍 ver_inventario": "!!ver_inventario - Veja os itens que você possui.",
        "👹 lutar_boss": "!!lutar_boss <nome_boss> - Lute contra um boss (ex: !!lutar_boss Zumbi Gigante, !!lutar_boss Mestre dos Zumbis).",
        "🗺️ missao": "!!missao - Receba uma missão diária para completar.",
        "💡 dica": "!!dica - Obtenha uma dica sobre sobrevivência.",
        "🏃 fuga": "!!fuga - Tente escapar de uma situação de perigo.",
        "⚔️ pvp": "!!pvp @usuario - Desafie outro jogador para uma batalha de PvP."
    }

    resposta = "🆘 **Comandos disponíveis:**\n" + "\n".join([f"{cmd}: {desc}" for cmd, desc in comandos.items()])
    await ctx.send(resposta)

# Executar o bot
TOKEN = os.getenv('TOKEN')
bot.run(TOKEN)
