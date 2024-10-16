from discord.ext import commands
from database import get_saldo, update_saldo, get_banco, update_banco
import random

class Banco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.apocalyptic_messages = [
            "A vida é um combate constante contra os horrores do mundo.",
            "Em tempos sombrios, cada moeda conta.",
            "Sobreviver é a verdadeira vitória neste mundo devastado.",
            "A escassez de recursos é uma luta diária, mas ainda temos esperança.",
            "O que é o dinheiro em um mundo onde a sobrevivência é tudo?",
            "Cada transação é uma batalha em nossa luta pela sobrevivência.",
        ]

    @commands.command(name="depositar")
    async def depositar(self, ctx, valor: int):
        if valor <= 0:
            await ctx.send("Você precisa depositar um valor positivo!")
            return

        saldo_atual = get_saldo(ctx.author.id)
        if valor > saldo_atual:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente para depositar {valor} moedas!")
            return

        update_saldo(ctx.author.id, -valor)
        novo_banco = update_banco(ctx.author.id, valor)
        await ctx.send(f"{ctx.author.mention}, você depositou {valor} moedas no banco. Saldo no banco agora é {novo_banco} moedas.")
        await ctx.send(random.choice(self.apocalyptic_messages))  # Mensagem apocalíptica

    @commands.command(name="sacar")
    async def sacar(self, ctx, valor: int):
        if valor <= 0:
            await ctx.send("Você precisa sacar um valor positivo!")
            return

        banco_atual = get_banco(ctx.author.id)
        if valor > banco_atual:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente no banco para sacar {valor} moedas!")
            return

        update_banco(ctx.author.id, -valor)
        novo_saldo = update_saldo(ctx.author.id, valor)
        await ctx.send(f"{ctx.author.mention}, você sacou {valor} moedas. Seu saldo atual é {novo_saldo} moedas.")
        await ctx.send(random.choice(self.apocalyptic_messages))  # Mensagem apocalíptica

    @commands.command(name="banco")
    async def banco(self, ctx):
        banco_atual = get_banco(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, seu saldo no banco é {banco_atual} moedas.")
        await ctx.send(random.choice(self.apocalyptic_messages))  # Mensagem apocalíptica

def setup(bot):
    bot.add_cog(Banco(bot))
