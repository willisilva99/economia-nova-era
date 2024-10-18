import discord
from discord.ext import commands
from discord import Embed
import os

# Configurações do bot
intents = discord.Intents.default()
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix="!!", intents=intents)

# Variáveis de pagamento (PIX, QR Code)
qr_code_link = "https://cdn.discordapp.com/attachments/1291144028590706799/1296617719029960814/IMG_20240715_155531.jpg"
pix_code = "00020126550014br.gov.bcb.pix0114+55679810387370215DOACAO NOVA ERA5204000053039865802BR5924Willi Aparecido Oliveira6008Brasilia62090505v56ir63049489"
ticket_channel_id = "1262580157130997760"  # ID do canal de tickets

# Função para iniciar o processo de compra de VIP
@bot.command(name="comprarvip")
async def comprar_vip(ctx):
    embed = Embed(
        title="Escolha seu Pacote VIP",
        description="Reaja para **ver os detalhes** de cada pacote:\n"
                    "💎 - Ver Pacote DIAMANTE\n"
                    "🥈 - Ver Pacote PRATA\n"
                    "🥉 - Ver Pacote BRONZE\n",
        color=discord.Color.blue()
    )
    embed.set_footer(text="Apenas o usuário que chamou o comando pode reagir.")

    # Envio da mensagem
    message = await ctx.send(embed=embed)

    # Adicionar reações
    await message.add_reaction("💎")
    await message.add_reaction("🥈")
    await message.add_reaction("🥉")

    # Função de verificação
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["💎", "🥈", "🥉"] and reaction.message.id == message.id

    try:
        # Esperar pela reação do usuário
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

        if str(reaction.emoji) == "💎":
            await mostrar_detalhes(ctx, "DIAMANTE", 60)
        elif str(reaction.emoji) == "🥈":
            await mostrar_detalhes(ctx, "PRATA", 30)
        elif str(reaction.emoji) == "🥉":
            await mostrar_detalhes(ctx, "BRONZE", 20)

    except Exception as e:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")

# Função para mostrar os detalhes de cada pacote VIP
async def mostrar_detalhes(ctx, pacote, valor):
    if pacote == "DIAMANTE":
        descricao = (
            "🎯 1 Sniper (Nível T6)\n"
            "🔋 2.000 Munições 7.62 AP\n"
            "🏍️ 1 Moto\n"
            "⚡ 1 Porrete Elétrico (Nível T6)\n"
            "🔧 1 Silenciador\n"
            "🔭 1 Mira 4x\n"
            "🪑 1 Mod Banco para 2 Pessoas\n"
            "⛽ 1 Mod de Combustível para Moto\n"
            "⛽ 3.000 Unidades de Combustível\n"
            "💬 Cargo no Discord: DIAMANTE"
        )
    elif pacote == "PRATA":
        descricao = (
            "🪖 AK-47 (Nível T6)\n"
            "🔫 1 Silenciador\n"
            "🔭 1 Mira 4x\n"
            "⛽ 5.000 Unidades de Gasolina\n"
            "🔋 2.000 Munições AP\n"
            "🏍️ 1 Moto\n"
            "💬 Cargo no Discord: PLATA"
        )
    elif pacote == "BRONZE":
        descricao = (
            "⛏️ 1 Picareta de Ferro\n"
            "🔧 1 Pá de Ferro\n"
            "🔨 1 Martelo\n"
            "🪨 1.000 Pedras Portuguesas\n"
            "🌲 1.000 Madeira\n"
            "🧱 200 Cimentos\n"
            "🔫 1 12 (Nível T6)\n"
            "🔋 200 Munições 12\n"
            "💬 Cargo no Discord: BRONZE"
        )

    embed = Embed(
        title=f"Detalhes do Pacote {pacote}",
        description=descricao,
        color=discord.Color.green()
    )
    embed.add_field(name="Preço", value=f"R${valor}", inline=False)
    embed.set_footer(text="Reaja com 💲 para ver o preço ou ↩️ para voltar à lista de pacotes.")

    message = await ctx.send(embed=embed)
    await message.add_reaction("💲")
    await message.add_reaction("↩️")

    def check_option(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["💲", "↩️"] and reaction.message.id == message.id

    try:
        # Espera o usuário escolher ver o preço ou voltar à lista
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_option)

        if str(reaction.emoji) == "💲":
            await mostrar_pagamento(ctx, pacote, valor)
        elif str(reaction.emoji) == "↩️":
            await comprar_vip(ctx)

    except Exception as e:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")

# Função para mostrar as informações de pagamento
async def mostrar_pagamento(ctx, pacote, valor):
    embed = Embed(
        title=f"Pacote {pacote} - R${valor}",
        description="Reaja para escolher uma das opções abaixo:\n"
                    "🖼️ - Ver QR Code para pagamento\n"
                    "📋 - Copiar código PIX\n"
                    "↩️ - Voltar para a lista de pacotes",
        color=discord.Color.green()
    )
    message = await ctx.send(embed=embed)
    await message.add_reaction("🖼️")
    await message.add_reaction("📋")
    await message.add_reaction("↩️")

    # Função para verificar a reação do usuário
    def check_payment_option(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🖼️", "📋", "↩️"] and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_payment_option)

        if str(reaction.emoji) == "🖼️":
            await enviar_qr_code(ctx)
            await confirmar_pagamento_reacao(ctx)
        elif str(reaction.emoji) == "📋":
            await copiar_pix(ctx)
            await confirmar_pagamento_reacao(ctx)
        elif str(reaction.emoji) == "↩️":
            await comprar_vip(ctx)

    except Exception as e:
        await ctx.send("Tempo esgotado. Por favor, tente novamente.")

# Função para exibir a opção de confirmar o pagamento após o QR Code ou o código PIX
async def confirmar_pagamento_reacao(ctx):
    embed = Embed(
        title="Pagamento Realizado?",
        description="Reaja com ✅ para confirmar que você já fez o pagamento.",
        color=discord.Color.orange()
    )
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")

    # Função para verificar a confirmação do pagamento
    def check_confirm(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id

    try:
        await bot.wait_for('reaction_add', timeout=600.0, check=check_confirm)
        await confirmar_pagamento(ctx)
    except Exception as e:
        await ctx.send("Tempo esgotado para confirmação. Caso tenha realizado o pagamento, por favor, entre em contato.")

# Função para enviar o QR Code diretamente como embed
async def enviar_qr_code(ctx):
    embed = Embed(
        title="QR Code para Pagamento",
        description="Use o QR Code abaixo para fazer o pagamento:",
        color=discord.Color.blue()
    )
    embed.set_image(url=qr_code_link)  # Definindo a imagem do QR Code diretamente no embed
    await ctx.send(embed=embed)

# Função para enviar o código PIX para copiar e colar
async def copiar_pix(ctx):
    embed = Embed(
        title="Código PIX para Copiar",
        description=f"**Código PIX:** `{pix_code}`\n\nCopie e cole no seu aplicativo bancário.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Função para confirmar o pagamento, enviar agradecimento e direcionar para o canal de tickets
async def confirmar_pagamento(ctx):
    embed = Embed(
        title="Pagamento Confirmado",
        description=f"Obrigado por seu pagamento! 🎉\n"
                    f"Agora, envie seu comprovante no canal de tickets: <#{ticket_channel_id}>.",
        color=discord.Color.gold()
    )
    await ctx.send(embed=embed)

    # Agradecimento ao usuário
    await ctx.send(f"Muito obrigado, {ctx.author.mention}, por sua compra! Estamos processando sua solicitação.")

# Rodar o bot
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
