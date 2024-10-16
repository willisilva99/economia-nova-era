import discord
from discord.ext import commands
import random
from database import update_saldo, get_saldo, adicionar_xp

class PvP(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pvp")
    async def pvp(self, ctx, adversario: discord.Member):
        if adversario == ctx.author:
            await ctx.send("Você não pode desafiar a si mesmo para um PvP!")
            return

        # Enviar a mensagem de desafio
        desafio = await ctx.send(f"{adversario.mention}, você foi desafiado para um PvP por {ctx.author.mention}! Reaja com ✅ para aceitar ou ❌ para recusar.")

        # Adiciona reações de aceitação e recusa
        await desafio.add_reaction("✅")
        await desafio.add_reaction("❌")

        # Função de verificação para garantir que a reação seja do adversário e seja válida
        def check(reaction, user):
            return user == adversario and str(reaction.emoji) in ["✅", "❌"] and reaction.message.id == desafio.id

        try:
            # Espera pela reação do adversário (timeout de 60 segundos)
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except TimeoutError:
            await ctx.send(f"{adversario.mention} não respondeu ao desafio de PvP a tempo.")
            return

        # Verifica se o adversário aceitou ou recusou
        if str(reaction.emoji) == "❌":
            await ctx.send(f"{adversario.mention} recusou o desafio de PvP!")
            return

        # Início do combate
        await ctx.send(f"{ctx.author.mention} e {adversario.mention} estão lutando! ⚔️")

        # Simulação de combate: Determina aleatoriamente o vencedor
        vencedor = random.choice([ctx.author, adversario])
        perdedor = adversario if vencedor == ctx.author else ctx.author

        # Recompensa para o vencedor
        recompensa = random.randint(20, 100)  # Valor aleatório de moedas
        xp_ganho = random.randint(10, 25)  # XP ganho

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
