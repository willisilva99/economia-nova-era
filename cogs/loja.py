import discord
from discord.ext import commands
from database import update_saldo, adicionar_item, get_saldo

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
        if nome_arma not in self.armas:
            await ctx.send(f"{ctx.author.mention}, essa arma não está disponível na loja.")
            return
        
        preco = self.armas[nome_arma]
        saldo = get_saldo(ctx.author.id)

        if saldo < preco:
            await ctx.send(f"{ctx.author.mention}, você não tem saldo suficiente para comprar {nome_arma}!")
            return

        update_saldo(ctx.author.id, -preco)
        adicionar_item(ctx.author.id, nome_arma)
        await ctx.send(f"{ctx.author.mention}, você comprou uma {nome_arma} por {preco} moedas!")

def setup(bot):
    bot.add_cog(Loja(bot))
