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
            ganho = random.randint(10, valor)
            novo_saldo = update_saldo(ctx.author.id, ganho)
            await ctx.send(f"🎉 Parabéns! Seu investimento teve sucesso e você ganhou {ganho} moedas! "
                           f"Seu novo saldo é {novo_saldo} moedas.\n"
                           f"**Lembre-se:** A esperança é a última que morre, continue investindo!")

        # Armazena o investimento
        if ctx.author.id in self.investimentos:
            self.investimentos[ctx.author.id] += valor
        else:
            self.investimentos[ctx.author.id] = valor

    @commands.command(name="ver_investimentos")
    async def ver_investimentos(self, ctx):
        total_investido = self.investimentos.get(ctx.author.id, 0)
        await ctx.send(f"{ctx.author.mention}, você investiu um total de {total_investido} moedas até agora.\n"
                       f"**Nota:** Em tempos difíceis, seu dinheiro pode ser tanto um aliado quanto um inimigo.")

    @commands.command(name="cancelar_investimento")
    async def cancelar_investimento(self, ctx):
        if ctx.author.id not in self.investimentos:
            await ctx.send(f"{ctx.author.mention}, você não tem investimentos ativos para cancelar.")
            return

        valor_investido = self.investimentos[ctx.author.id]
        penalidade = random.randint(5, valor_investido // 4)
        valor_recuperado = valor_investido - penalidade
        update_saldo(ctx.author.id, valor_recuperado)
        del self.investimentos[ctx.author.id]

        await ctx.send(f"⚠️ Você cancelou seu investimento e recuperou {valor_recuperado} moedas, "
                       f"mas perdeu {penalidade} moedas como penalidade.\n"
                       f"**Lembre-se:** No apocalipse, decisões precipitadas podem custar caro.")

    @investir.error
    async def investir_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            tempo_espera = int(error.retry_after // 60)
            await ctx.send(f"⏳ Espere mais {tempo_espera} minutos antes de investir novamente.")
        else:
            await ctx.send("Ocorreu um erro ao tentar investir.")

def setup(bot):
    bot.add_cog(Investimento(bot))
