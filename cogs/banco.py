from discord.ext import commands
from database import get_saldo, update_saldo, get_banco, update_banco

class Banco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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

def setup(bot):
    bot.add_cog(Banco(bot))
