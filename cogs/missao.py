import discord
from discord.ext import commands
import random
from database import obter_inventario, update_saldo  # Importar funções necessárias

class Missao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.missoes = [
            {
                "descricao": "Ajude um sobrevivente a encontrar suprimentos!",
                "arma_requerida": None,  # Não requer arma
                "recompensa": 50
            },
            {
                "descricao": "Derrote 5 zumbis em sua área!",
                "arma_requerida": "Espada_Enferrujada",
                "recompensa": 100
            },
            {
                "descricao": "Colete recursos de uma loja abandonada!",
                "arma_requerida": "Arco_e_Flecha",
                "recompensa": 75
            },
            {
                "descricao": "Proteja um abrigo contra ataques de zumbis!",
                "arma_requerida": "Fuzil_Assalto",
                "recompensa": 150
            },
            {
                "descricao": "Encontre um esconderijo seguro e proteja-o!",
                "arma_requerida": "Granada",
                "recompensa": 120
            },
            {
                "descricao": "Recupere um carro de um estacionamento abandonado!",
                "arma_requerida": "Machado",
                "recompensa": 80
            },
            {
                "descricao": "Resgate um grupo de sobreviventes cercados!",
                "arma_requerida": "Fuzil_Assalto",
                "recompensa": 200
            },
            {
                "descricao": "Explore uma zona radioativa em busca de recursos raros!",
                "arma_requerida": "Cajado_Mágico",
                "recompensa": 250
            },
            {
                "descricao": "Defenda um grupo de sobreviventes de uma horda de zumbis!",
                "arma_requerida": "Katana",
                "recompensa": 300
            },
            {
                "descricao": "Destrua um ninho de zumbis em uma área perigosa!",
                "arma_requerida": "Fuzil_Assalto",
                "recompensa": 150
            }
        ]

    @commands.command(name="missao")
    async def missao(self, ctx):
        missao_selecionada = random.choice(self.missoes)
        inventario = obter_inventario(ctx.author.id)

        # Verifica se a missão requer uma arma específica
        if missao_selecionada["arma_requerida"] and missao_selecionada["arma_requerida"] not in inventario:
            await ctx.send(f"🎯 **Nova missão:** {missao_selecionada['descricao']} (Requer: {missao_selecionada['arma_requerida'].replace('_', ' ')})\n"
                           f"🔒 Você não possui a arma necessária para esta missão.")
            return
        
        # Se o jogador aceitar a missão, simule a conclusão
        await ctx.send(f"🎯 **Nova missão:** {missao_selecionada['descricao']}")
        
        # Simulando a conclusão da missão com sucesso
        await ctx.send(f"✅ Você completou a missão e ganhou {missao_selecionada['recompensa']} moedas!")

        # Atualiza o saldo do jogador
        update_saldo(ctx.author.id, missao_selecionada['recompensa'])  # Atualiza o saldo do jogador

def setup(bot):
    bot.add_cog(Missao(bot))
