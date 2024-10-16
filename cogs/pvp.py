import discord
from discord.ext import commands
import random
from database import update_saldo, get_saldo, obter_inventario, adicionar_xp

class PvP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Bônus de cada arma
        self.arma_bonus = {
            "Faca": 5,
            "Pistola": 15,
            "Arma de Fogo": 20,
            "Espada": 10,
            "Arco e Flecha": 8
        }

    @commands.command(name="pvp")
    async def pvp(self, ctx, adversario: discord.Member):
        if adversario == ctx.author:
            await ctx.send("Você não pode desafiar a si mesmo para um PvP!")
            return

        # Enviar a mensagem de desafio
        desafio = await ctx.send(f"{adversario.mention}, você foi desafiado para um PvP por {ctx.author.mention}! Reaja com ✅ para aceitar ou ❌ para recusar.")
        await desafio.add_reaction("✅")
        await desafio.add_reaction("❌")

        # Verificação da reação
        def check(reaction, user):
            return user == adversario and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == desafio.id

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send(f"{adversario.mention} não respondeu ao desafio de PvP a tempo.")
            return

        if str(reaction.emoji) == "❌":
            await ctx.send(f"{adversario.mention} recusou o desafio de PvP!")
            return

        # Obter os inventários dos jogadores
        inventario_desafiante = obter_inventario(ctx.author.id)
        inventario_adversario = obter_inventario(adversario.id)

        # Calcular os bônus de combate com base nas armas
        bonus_desafiante = sum(self.arma_bonus.get(arma, 0) for arma in inventario_desafiante)
        bonus_adversario = sum(self.arma_bonus.get(arma, 0) for arma in inventario_adversario)

        # Determinar o vencedor com base no bônus
        total = bonus_desafiante + bonus_adversario
        prob_desafiante = bonus_desafiante / total if total > 0 else 0.5
        vencedor = ctx.author if random.random() < prob_desafiante else adversario
        perdedor = adversario if vencedor == ctx.author else ctx.author

        # Recompensa para o vencedor
        recompensa = random.randint(20, 100)
        xp_ganho = random.randint(10, 25)

        update_saldo(vencedor.id, recompensa)
        adicionar_xp(vencedor.id, xp_ganho)

        # Resultado do combate
        await ctx.send(f"🏆 {vencedor.mention} venceu a batalha e ganhou {recompensa} moedas e {xp_ganho} de XP!")
        await ctx.send(f"😞 {perdedor.mention} foi derrotado. Tente novamente mais tarde!")

    @pvp.error
    async def pvp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Por favor, mencione o usuário que deseja desafiar para o PvP. Exemplo: `!!pvp @usuario`")
        else:
            await ctx.send("Ocorreu um erro ao tentar iniciar o PvP.")

def setup(bot):
    bot.add_cog(PvP(bot))
