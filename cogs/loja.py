import discord
from discord.ext import commands

class Loja(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.armas = {
            "Espada Enferrujada": 150,
            "Arco e Flecha": 200,
            "Fuzil de Assalto": 500,
            "Granada": 300,
            "Machado": 250,
            "Katana": 400,
            "Clava de Ferro": 350,
        }

    @commands.command(name="listar_armas")
    async def listar_armas(self, ctx):
        lista_armas = "\n".join([f"{arma}: {preco} moedas" for arma, preco in self.armas.items()])
        await ctx.send(f"🛒 **Armas disponíveis na loja:**\n{lista_armas}")

    @commands.command(name="comprar")
    async def comprar(self, ctx, nome_arma: str):
        # Lógica de compra aqui...

def setup(bot):
    bot.add_cog(Loja(bot))
