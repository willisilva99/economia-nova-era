from discord.ext import commands
import random
from database import update_saldo

class Trabalho(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trabalho_opcoes = [
            {"tipo": "Caçador", "salario": random.randint(70, 150)},
            {"tipo": "Coletor de Recursos", "salario": random.randint(50, 100)},
            {"tipo": "Procurador de Abrigos", "salario": random.randint(100, 200)},
            {"tipo": "Zumbi Caçado", "salario": random.randint(30, 80)},
            {"tipo": "Agricultor", "salario": random.randint(20, 50)},
            {"tipo": "Vigilante", "salario": random.randint(15, 40)},
            {"tipo": "Fugitivo", "salario": random.randint(10, 30)},
        ]

    @commands.command(name="trabalho")
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hora de cooldown
    async def trabalho(self, ctx):
        trabalho_selecionado = random.choice(self.trabalho_opcoes)
        salario = trabalho_selecionado["salario"]
        tipo = trabalho_selecionado["tipo"]

        # Eventos aleatórios com maior chance de perda de moedas
        evento = random.choice([
            None,
            "Você encontrou um suprimento extra!",
            "Um grupo de zumbis tentou atacá-lo, mas você conseguiu se defender!",
            "Você se machucou durante a caça e perdeu algumas moedas.",
            "Você se distraiu e perdeu algumas moedas enquanto trabalhava!"
        ])

        # Chance de perder moedas
        if evento in ["Você se machucou durante a caça e perdeu algumas moedas.", 
                      "Você se distraiu e perdeu algumas moedas enquanto trabalhava!"]:
            perda = random.randint(5, 30)
            salario -= perda
            await ctx.send(f"Infelizmente, você perdeu {perda} moedas devido a um incidente.")

        # Atualiza o saldo do usuário
        novo_saldo = update_saldo(ctx.author.id, salario)

        # Mensagem de retorno
        await ctx.send(f"{ctx.author.mention}, você trabalhou como **{tipo}** e ganhou {salario} moedas! Seu saldo atual é {novo_saldo} moedas.")

        # Mensagem do evento
        if evento:
            await ctx.send(evento)

    @trabalho.error
    async def trabalho_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            tempo_espera = int(error.retry_after // 60)
            await ctx.send(f"⚠️ **Atenção!** Você deve esperar {tempo_espera} minutos antes de trabalhar novamente. "
                           f"Os zumbis estão rondando e cada minuto é precioso! Prepare-se antes de sair novamente.")
        else:
            await ctx.send("Ocorreu um erro ao tentar trabalhar.")

def setup(bot):
    bot.add_cog(Trabalho(bot))
