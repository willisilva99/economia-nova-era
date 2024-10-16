import discord
from discord.ext import commands
from database import adicionar_item, obter_inventario

class Inventario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Definindo armas com seus respectivos bônus de dano
        self.armas_com_bonus = {
            "Espada Enferrujada": 5,
            "Arco e Flecha": 10,
            "Fuzil de Assalto": 20,
            "Granada": 15,
            "Machado": 12,
            "Katana": 25,
            "Clava de Ferro": 8,
        }

    @commands.command(name="adicionar_item")
    async def adicionar_item_cmd(self, ctx, item: str):
        if item not in self.armas_com_bonus:
            await ctx.send(f"{ctx.author.mention}, essa arma não é válida!")
            return
        adicionar_item(ctx.author.id, item)  # Adiciona o item ao inventário no banco de dados
        await ctx.send(f"{ctx.author.mention}, você adicionou **{item}** ao seu inventário!")

    @commands.command(name="ver_inventario")
    async def ver_inventario(self, ctx):
        inventario = obter_inventario(ctx.author.id)
        if not inventario:
            await ctx.send(f"{ctx.author.mention}, seu inventário está vazio.")
            return

        await ctx.send(f"📦 **Seu Inventário:**\n" + "\n".join(inventario))

def setup(bot):
    bot.add_cog(Inventario(bot))
