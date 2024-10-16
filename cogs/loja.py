import discord
from discord.ext import commands
from database import update_saldo, adicionar_item, get_saldo

class Loja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Armas disponíveis com nomes sem espaços
        self.armas = {
            "Espada_Enferrujada": 150,
            "Arco_e_Flecha": 200,
            "Fuzil_Assalto": 500,
            "Granada": 300,
            "Machado": 250,
            "Katana": 400,
            "Clava_Ferro": 350,
            "Lanca": 180,
            "Besta": 220,
            "Cajado_Magico": 600,
            "Martelo_Guerra": 450,
            "Adaga": 120,
            "Bomba": 350
        }

    @commands.command(name="listar_armas")
    async def listar_armas(self, ctx):
        lista_armas = "\n".join([f"{arma.replace('_', ' ')}: {preco} moedas" for arma, preco in self.armas.items()])
        await ctx.send(f"🛒 **Armas disponíveis na loja:**\n{lista_armas}")

    @commands.command(name="comprar")
    async def comprar(self, ctx, nome_arma: str):
        # Remove espaços e converte para o formato correto
        nome_arma_formatado = nome_arma.replace(" ", "_")

        # Verifica se a arma está na lista de armas disponíveis
        if nome_arma_formatado not in self.armas:
            await ctx.send(f"{ctx.author.mention}, essa arma não está disponível na loja.")
            return
        
        preco = self.armas[nome_arma_formatado]
        saldo = get_saldo(ctx.author.id)  # Obtém o saldo do usuário

        # Verifica se o saldo é suficiente para a compra
        if saldo < preco:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente para comprar {nome_arma_formatado.replace('_', ' ')}!")
            return

        # Atualiza o saldo e adiciona a arma ao inventário
        update_saldo(ctx.author.id, -preco)
        adicionar_item(ctx.author.id, nome_arma_formatado)
        await ctx.send(f"{ctx.author.mention}, você comprou uma {nome_arma_formatado.replace('_', ' ')} por {preco} moedas!")

def setup(bot):
    bot.add_cog(Loja(bot))
