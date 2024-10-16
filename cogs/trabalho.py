from discord.ext import commands
import random
from database import update_saldo, get_saldo, obter_inventario, adicionar_item

class Trabalho(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trabalho_opcoes = [
            {"tipo": "Caçador", "salario": random.randint(70, 150)},
            {"tipo": "Coletor de Recursos", "salario": random.randint(50, 100)},
            {"tipo": "Procurador de Abrigos", "salario": random.randint(100, 200)},
            {"tipo": "Agricultor", "salario": random.randint(20, 50)},
            {"tipo": "Vigilante", "salario": random.randint(15, 40)},
            {"tipo": "Fugitivo", "salario": random.randint(10, 30)},
        ]
        self.ferramentas_roubo = ["Faca", "Pistola", "Arma de Fogo"]  # Ferramentas necessárias para roubo

    @commands.command(name="trabalho")
    @commands.cooldown(1, 3600, commands.BucketType.user)  # 1 hora de cooldown
    async def trabalho(self, ctx):
        trabalho_selecionado = random.choice(self.trabalho_opcoes)
        salario = trabalho_selecionado["salario"]
        tipo = trabalho_selecionado["tipo"]

        evento = random.choice([
            None,
            "Você encontrou um suprimento extra!",
            "Um grupo de zumbis tentou atacá-lo, mas você conseguiu se defender!",
            "Você se machucou durante a caça e perdeu algumas moedas.",
            "Você se distraiu e perdeu algumas moedas enquanto trabalhava!"
        ])

        if evento in ["Você se machucou durante a caça e perdeu algumas moedas.", 
                      "Você se distraiu e perdeu algumas moedas enquanto trabalhava!"]:
            perda = random.randint(5, 30)
            salario -= perda
            await ctx.send(f"Infelizmente, você perdeu {perda} moedas devido a um incidente.")

        novo_saldo = update_saldo(ctx.author.id, salario)
        await ctx.send(f"{ctx.author.mention}, você trabalhou como **{tipo}** e ganhou {salario} moedas! Seu saldo atual é {novo_saldo} moedas.")

        if evento:
            await ctx.send(evento)

    @commands.command(name="comprar")
    async def comprar(self, ctx, nome_ferramenta: str):
        preco_ferramenta = 100  # Defina um preço para as ferramentas de roubo
        saldo = get_saldo(ctx.author.id)

        if saldo < preco_ferramenta:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente para comprar {nome_ferramenta}!")
            return

        if nome_ferramenta not in self.ferramentas_roubo:
            await ctx.send(f"{ctx.author.mention}, essa ferramenta não está disponível na loja.")
            return

        # Deduz o preço do saldo e adiciona a ferramenta ao inventário
        update_saldo(ctx.author.id, -preco_ferramenta)
        adicionar_item(ctx.author.id, nome_ferramenta)
        await ctx.send(f"{ctx.author.mention}, você comprou uma {nome_ferramenta} por {preco_ferramenta} moedas!")

    @commands.command(name="roubar")
    async def roubar(self, ctx, membro: discord.Member):
        if membro == ctx.author:
            await ctx.send("Você não pode roubar a si mesmo!")
            return

        # Verifica se o usuário tem uma ferramenta de roubo
        inventario = obter_inventario(ctx.author.id)
        if not any(item in inventario for item in self.ferramentas_roubo):
            await ctx.send(f"{ctx.author.mention}, você precisa de uma ferramenta de roubo para tentar roubar!")
            return

        # Lógica para roubar
        sucesso = random.choice([True, False])  # 50% de chance de sucesso
        if sucesso:
            valor_roubado = random.randint(10, 100)  # Valor a ser roubado
            saldo_membro = get_saldo(membro.id)

            if saldo_membro < valor_roubado:
                await ctx.send(f"{ctx.author.mention}, {membro.mention} não tem saldo suficiente para ser roubado!")
                return

            # Deduz o valor do saldo do membro
            update_saldo(membro.id, -valor_roubado)
            update_saldo(ctx.author.id, valor_roubado)  # Adiciona o valor ao saldo do ladrão
            await ctx.send(f"{ctx.author.mention}, você roubou {valor_roubado} moedas de {membro.mention}!")
        else:
            await ctx.send(f"{ctx.author.mention}, você falhou na tentativa de roubo! Um zumbi apareceu e te assustou!")

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
