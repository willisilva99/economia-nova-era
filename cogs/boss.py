import discord
from discord.ext import commands
import random

class Boss(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Novos bosses com saúde e dano
        self.bosses = {
            "Zumbi Mutante": {"saude": 300, "dano": 50},
            "Chefe Zumbi": {"saude": 500, "dano": 80},
            "Líder do Culto": {"saude": 1000, "dano": 100},
            "Criatura das Sombras": {"saude": 700, "dano": 70},
            "Andarilho Enlouquecido": {"saude": 400, "dano": 60},
            "Esqueleto Vingador": {"saude": 350, "dano": 55},  # Novo boss
            "Mutante de Ferro": {"saude": 800, "dano": 90},  # Novo boss
            "Mestre dos Zumbis": {"saude": 1200, "dano": 120},  # Novo boss
            "Zumbi Gigante": {"saude": 1500, "dano": 150},  # Novo boss
            "Fantasma Errante": {"saude": 600, "dano": 75}  # Novo boss
        }

    @commands.command(name="lutar_boss")
    async def lutar_boss(self, ctx, nome_boss: str):
        if nome_boss not in self.bosses:
            await ctx.send(f"{ctx.author.mention}, esse boss não existe. Tente com um dos seguintes:\n" + "\n".join(self.bosses.keys()))
            return
        
        boss = self.bosses[nome_boss]
        saude_boss = boss["saude"]

        await ctx.send(f"⚔️ Você começou a luta contra **{nome_boss}** com {saude_boss} de saúde!")

        while saude_boss > 0:
            dano_jogador = random.randint(20, 50)  # Dano que o jogador causa

            saude_boss -= dano_jogador

            await ctx.send(f"Você causou {dano_jogador} de dano a **{nome_boss}**! Saúde restante: {saude_boss}")

            if saude_boss <= 0:
                # Jogador venceu
                recompensa = random.randint(100, 300)  # Recompensa por vencer
                await ctx.send(f"🎉 Você derrotou **{nome_boss}**! Você ganhou {recompensa} moedas!")
                break

            # Boss ataca
            dano_boss = boss["dano"]
            await ctx.send(f"**{nome_boss}** atacou e causou {dano_boss} de dano em você!")

def setup(bot):
    bot.add_cog(Boss(bot))
