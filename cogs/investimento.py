from discord.ext import commands
import random
from database import update_saldo, get_saldo

class Investimento(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="investir")
    @commands.cooldown(1, 7200, commands.BucketType.user)  # 2 horas de cooldown
    async def investir(self, ctx, valor: int):
        saldo_atual = get_saldo(ctx.author.id)

        if valor <= 0:
            await ctx.send("Você precisa investir um valor positivo!")
            return

        if valor > saldo_atual:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente para investir {valor} moedas!")
            return

        chance = random.random()
        if chance < 0.5:
            ganho = valor * random.uniform(0.5, 1.5)
            novo_saldo = update_saldo(ctx.author.id, int(ganho))
            await ctx.send(f"{ctx.author.mention}, seu investimento foi um sucesso! Você ganhou {int(ganho)} moedas! Seu saldo atual é {novo_saldo} moedas.")
        else:
            perda = valor * random.uniform(0.5, 1)
            novo_saldo = update_saldo(ctx.author.id, -int(perda))
            await ctx.send(f"{ctx.author.mention}, infelizmente, você perdeu {int(perda)} moedas com seu investimento. Seu saldo atual é {novo_saldo} moedas.")

    @investir.error
    async def investir_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Espere mais {int(error.retry_after // 60)} minutos para investir novamente.")
        else:
            await ctx.send("Ocorreu um erro ao tentar investir.")

def setup(bot):
    bot.add_cog(Investimento(bot))
