from discord.ext import commands
import random
from database import get_saldo, update_saldo

class Investimento(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.investimentos = {}  # Armazena investimentos por usuário

    @commands.command(name="investir")
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hora de cooldown
    async def investir(self, ctx, valor: int):
        if valor <= 0:
            await ctx.send("Você precisa investir um valor positivo!")
            return

        saldo_atual = get_saldo(ctx.author.id)
        if valor > saldo_atual:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente para investir {valor} moedas!")
            return

        # Decidir aleatoriamente o resultado do investimento
        chance_perda = random.randint(1, 100)
        if chance_perda <= 50:  # 50% de chance de perder moedas
            perda = random.randint(10, valor // 2)
            novo_saldo = update_saldo(ctx.author.id, -perda)
            await ctx.send(f"💸 Infelizmente, seu investimento não deu certo e você perdeu {perda} moedas. "
                           f"Seu novo saldo é {novo_saldo} moedas.\n"
                           f"**Dica:** Sobreviver neste mundo é um jogo de riscos. Cada decisão conta!")
        else:
            ganho = random.randint(10, valor
