from discord.ext import commands
from database import get_saldo, get_banco

class Saldo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="saldo")
    async def saldo(self, ctx):
        saldo_atual = get_saldo(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, seu saldo atual é {saldo_atual} moedas.")

    @commands.command(name="saldo_banco")
    async def saldo_banco(self, ctx):
        banco_atual = get_banco(ctx.author.id)
        await ctx.send(f"{ctx.author.mention}, seu saldo no banco é {banco_atual} moedas.")

def setup(bot):
    bot.add_cog(Saldo(bot))
