import discord
from discord.ext import commands
from database import get_saldo, get_xp, adicionar_xp, update_saldo  # Certifique-se de que essas funções existem
import random

class Nivel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def calcular_nivel(self, xp):
        # Define a lógica para calcular o nível com base na XP
        return int(xp ** 0.5)  # Exemplo simples de cálculo de nível

    def xp_para_proximo_nivel(self, nivel):
        # Defina a quantidade de XP necessária para o próximo nível
        return (nivel + 1) ** 2  # Aumenta a XP necessária para cada nível

    @commands.command(name="trabalhar")
    async def trabalhar(self, ctx):
        # Simula a ação de trabalhar e ganha XP
        xp_ganho = random.randint(20, 50)
        adicionar_xp(ctx.author.id, xp_ganho)  # Atualiza a XP do usuário no banco de dados

        xp_total = get_xp(ctx.author.id)  # Obtém a XP total atual do usuário
        nivel_atual = self.calcular_nivel(xp_total)
        xp_necessaria = self.xp_para_proximo_nivel(nivel_atual)

        await ctx.send(f"💼 Você trabalhou e ganhou {xp_ganho} XP! Total: {xp_total} XP.")

        # Verifica se o usuário subiu de nível
        if xp_total >= xp_necessaria:
            await ctx.send(f"🎉 Parabéns {ctx.author.mention}, você subiu para o nível {nivel_atual + 1}!")

    @commands.command(name="nivel")
    async def nivel(self, ctx):
        # Obtém a XP do usuário do banco de dados
        xp_total = get_xp(ctx.author.id)
        nivel_atual = self.calcular_nivel(xp_total)
        xp_necessaria = self.xp_para_proximo_nivel(nivel_atual)

        await ctx.send(f"🎖️ {ctx.author.mention}, você está no nível {nivel_atual} com {xp_total} XP.\n"
                       f"Para subir para o nível {nivel_atual + 1}, você precisa de {xp_necessaria - xp_total} XP a mais!")

def setup(bot):
    bot.add_cog(Nivel(bot))
