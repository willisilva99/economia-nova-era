from discord.ext import commands
import random
from database import update_saldo

class Trabalho(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="trabalho")
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hora de cooldown
    async def trabalho(self, ctx):
        salario = random.randint(50, 150)
        novo_saldo = update_saldo(ctx.author.id, salario)
        await ctx.send(f"{ctx.author.mention}, você trabalhou e ganhou {salario} moedas! Seu saldo atual é {novo_saldo} moedas.")

    @trabalho.error
    async def trabalho_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Espere mais {int(error.retry_after // 60)} minutos para trabalhar novamente.")
        else:
            await ctx.send("Ocorreu um erro ao tentar trabalhar.")

def setup(bot):
    bot.add_cog(Trabalho(bot))
