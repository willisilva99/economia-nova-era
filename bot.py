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

# Link da imagem inicial para o comando !!comprarvip
image_link = "https://cdn.discordapp.com/attachments/1291144028590706799/1296634863176122399/DALLE_2024-10-17_21.20.39_-_A_survivor_in_a_post-apocalyptic_world_inside_a_dimly_lit_makeshift_shop._The_survivor_is_standing_at_a_counter_choosing_from_a_variety_of_weapons_f.jpg"

# Links das imagens para cada pacote VIP
image_diamante = "https://cdn.discordapp.com/attachments/1291144028590706799/1296639105022693486/DALLE_2024-10-17_22.00.36_-_A_scene_showing_a_person_in_a_post-apocalyptic_setting_opening_a_special_drop_box_labeled_Diamante_Caixa_de_Drop._The_box_has_a_metallic_futuristic.webp"
image_prata = "https://cdn.discordapp.com/attachments/1291144028590706799/1296636697085476915/DALLE_2024-10-17_21.50.02_-_A_scene_showing_a_person_in_a_post-apocalyptic_setting_opening_a_special_drop_box_labeled_Prata_Caixa_de_Drop._The_box_has_a_metallic_silver_appeara.webp"
image_bronze = "https://cdn.discordapp.com/attachments/1291144028590706799/1296636677770449007/DALLE_2024-10-17_21.50.38_-_A_scene_in_a_post-apocalyptic_environment_where_a_person_is_opening_a_special_drop_box_labeled_Bronze_Caixa_de_Drop._The_box_has_a_rugged_bronze-co.webp"

# Imagem das formas de pagamento
image_pagamento = "https://cdn.discordapp.com/attachments/1291144028590706799/1296644402248417331/DALLE_2024-10-17_22.20.45_-_A_post-apocalyptic_scene_showing_a_person_making_a_payment_at_a_high-tech_portal_with_a_sign_in_the_background_reading_Nova_Era._The_portal_has_glo.webp"

# Dicionário para armazenar o inventário dos jogadores
user_inventory = {}

# Função para iniciar o processo de compra de VIP
@bot.command(name="comprarvip")
async def comprar_vip(ctx):
    embed = Embed(
        title="💠 **Escolha Seu Pacote VIP**",
        description=(
            "🛠️ Reaja para **ver os detalhes** de cada pacote:\n\n"
            "💎 - **Pacote DIAMANTE** - O mais completo, para sobreviventes de elite.\n"
            "🥈 - **Pacote PRATA** - Equipamento balanceado para se manter no apocalipse.\n"
            "🥉 - **Pacote BRONZE** - Inicie sua jornada com o básico necessário."
        ),
        color=discord.Color.blue()
    )
    embed.set_image(url=image_link)
    embed.set_footer(text="Reaja abaixo para escolher um pacote.")
    
    # Envio da mensagem
    message = await ctx.send(embed=embed)

    # Adicionar reações
    await message.add_reaction("💎")
    await message.add_reaction("🥈")
    await message.add_reaction("🥉")

    # Função de verificação
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["💎", "🥈", "🥉"] and reaction.message.id == message.id

    # Função para bloquear reações de outros jogadores
    def check_invalid_reaction(reaction, user):
        return user != ctx.author and reaction.message.id == message.id

    try:
        # Esperar pela reação do usuário
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

        # Apagar a mensagem anterior para limpar a interface
        await message.delete()

        # Mostrar detalhes do pacote escolhido
        if str(reaction.emoji) == "💎":
            await mostrar_detalhes(ctx, "DIAMANTE", 60, image_diamante)
        elif str(reaction.emoji) == "🥈":
            await mostrar_detalhes(ctx, "PRATA", 30, image_prata)
        elif str(reaction.emoji) == "🥉":
            await mostrar_detalhes(ctx, "BRONZE", 20, image_bronze)

    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado!** Por favor, tente novamente.")

    # Se um jogador diferente reagir
    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_invalid_reaction)
        await ctx.send(f"🚫 {user.mention}, você não pode reagir a este comando. Apenas {ctx.author.mention} pode interagir.")
    except:
        pass

# Função para mostrar os detalhes de cada pacote VIP, com a imagem correspondente
async def mostrar_detalhes(ctx, pacote, valor, imagem):
    if pacote == "DIAMANTE":
        descricao = (
            "💎 **Pacote DIAMANTE** 💎\n"
            "🔫 1 Sniper (Nível T6)\n"
            "🔋 2.000 Munições 7.62 AP\n"
            "🏍️ 1 Moto\n"
            "⚡ 1 Porrete Elétrico (Nível T6)\n"
            "🔧 1 Silenciador\n"
            "🔭 1 Mira 4x\n"
            "🪑 1 Mod Banco para 2 Pessoas\n"
            "⛽ 1 Mod de Combustível para Moto\n"
            "⛽ 3.000 Unidades de Combustível\n"
            "💬 Cargo no Discord: **DIAMANTE**"
        )
    elif pacote == "PRATA":
        descricao = (
            "🥈 **Pacote PRATA** 🥈\n"
            "🪖 AK-47 (Nível T6)\n"
            "🔫 1 Silenciador\n"
            "🔭 1 Mira 4x\n"
            "⛽ 5.000 Unidades de Gasolina\n"
            "🔋 2.000 Munições AP\n"
            "🏍️ 1 Moto\n"
            "💬 Cargo no Discord: **PLATA**"
        )
    elif pacote == "BRONZE":
        descricao = (
            "🥉 **Pacote BRONZE** 🥉\n"
            "⛏️ 1 Picareta de Ferro\n"
            "🔧 1 Pá de Ferro\n"
            "🔨 1 Martelo\n"
            "🪨 1.000 Pedras Portuguesas\n"
            "🌲 1.000 Madeira\n"
            "🧱 200 Cimentos\n"
            "🔫 1 12 (Nível T6)\n"
            "🔋 200 Munições 12\n"
            "💬 Cargo no Discord: **BRONZE**"
        )

    embed = Embed(
        title=f"🔍 **Detalhes do Pacote {pacote}**",
        description=descricao,
        color=discord.Color.green()
    )
    embed.add_field(name="💵 **Preço**", value=f"R${valor}", inline=False)
    embed.set_image(url=imagem)
    embed.set_footer(text="Reaja com 💲 para ver o preço ou ↩️ para voltar à lista de pacotes.")

    message = await ctx.send(embed=embed)
    await message.add_reaction("💲")
    await message.add_reaction("↩️")

    def check_option(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["💲", "↩️"] and reaction.message.id == message.id

    try:
        # Espera o usuário escolher ver o preço ou voltar à lista
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_option)

        # Apagar a mensagem anterior
        await message.delete()

        if str(reaction.emoji) == "💲":
            await mostrar_pagamento(ctx, pacote, valor)
        elif str(reaction.emoji) == "↩️":
            await comprar_vip(ctx)

    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado!** Por favor, tente novamente.")

# Função para mostrar as informações de pagamento com imagem personalizada
async def mostrar_pagamento(ctx, pacote, valor):
    embed = Embed(
        title=f"💳 **Pagamento do Pacote {pacote}** - R${valor}",
        description="Reaja para escolher uma das opções abaixo:\n"
                    "🖼️ - Ver **QR Code** para pagamento\n"
                    "📋 - Copiar **código PIX**\n"
                    "↩️ - Voltar para a lista de pacotes",
        color=discord.Color.gold()
    )
    embed.set_image(url=image_pagamento)  # Mostra a imagem personalizada das formas de pagamento
    message = await ctx.send(embed=embed)
    await message.add_reaction("🖼️")
    await message.add_reaction("📋")
    await message.add_reaction("↩️")

    # Função para verificar a reação do usuário
    def check_payment_option(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🖼️", "📋", "↩️"] and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_payment_option)

        # Apagar a mensagem anterior
        await message.delete()

        if str(reaction.emoji) == "🖼️":
            await enviar_qr_code(ctx)
            await confirmar_pagamento_reacao(ctx, "QR Code exibido. Realize o pagamento e confirme.")
        elif str(reaction.emoji) == "📋":
            await copiar_pix(ctx)
            await confirmar_pagamento_reacao(ctx, "Código PIX copiado. Realize o pagamento e confirme.")
        elif str(reaction.emoji) == "↩️":
            await comprar_vip(ctx)

    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado!** Por favor, tente novamente.")

# Função para exibir a opção de confirmar o pagamento após o QR Code ou o código PIX, com mensagem personalizada
async def confirmar_pagamento_reacao(ctx, mensagem):
    embed = Embed(
        title="✅ **Confirmar Pagamento**",
        description=mensagem + "\n\nReaja com ✅ para confirmar que o pagamento foi realizado.",
        color=discord.Color.orange()
    )
    message = await ctx.send(embed=embed)
    await message.add_reaction("✅")

    def check_confirm(reaction, user):
        return user == ctx.author and str(reaction.emoji) == "✅" and reaction.message.id == message.id

    try:
        await bot.wait_for('reaction_add', timeout=600.0, check=check_confirm)
        await confirmar_pagamento(ctx)
    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado para confirmação**. Caso tenha realizado o pagamento, por favor, entre em contato.")

# Função para enviar o QR Code diretamente como embed
async def enviar_qr_code(ctx):
    embed = Embed(
        title="📲 **QR Code para Pagamento**",
        description="Use o QR Code abaixo para fazer o pagamento:",
        color=discord.Color.blue()
    )
    embed.set_image(url=qr_code_link)  # Definindo a imagem do QR Code diretamente no embed
    await ctx.send(embed=embed)

# Função para enviar o código PIX para copiar e colar
async def copiar_pix(ctx):
    embed = Embed(
        title="📋 **Código PIX para Copiar**",
        description=f"**Código PIX:** `{pix_code}`\n\nCopie e cole no seu aplicativo bancário.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

# Função para confirmar o pagamento, enviar agradecimento e direcionar para o canal de tickets
async def confirmar_pagamento(ctx):
    embed = Embed(
        title="✅ **Pagamento Confirmado!**",
        description=f"🎉 Obrigado por seu pagamento!\n\n"
                    f"Agora, envie seu comprovante no canal de tickets: <#{ticket_channel_id}>.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed)

    # Agradecimento ao usuário
    await ctx.send(f"🎉 Muito obrigado, {ctx.author.mention}, por sua compra! Estamos processando sua solicitação.")

    # Adiciona o pacote VIP ao inventário do usuário
    adicionar_inventario(ctx.author.id, "VIP " + pacote)

# Função para adicionar o pacote ao inventário do jogador
def adicionar_inventario(user_id, pacote):
    if user_id not in user_inventory:
        user_inventory[user_id] = []
    user_inventory[user_id].append(pacote)

# Comando para verificar o inventário do jogador
@bot.command(name="inventario")
async def ver_inventario(ctx):
    user_id = ctx.author.id
    if user_id not in user_inventory or not user_inventory[user_id]:
        await ctx.send(f"📦 {ctx.author.mention}, seu inventário está vazio.")
    else:
        pacotes = ", ".join(user_inventory[user_id])
        await ctx.send(f"📦 {ctx.author.mention}, seu inventário: {pacotes}")

# Rodar o bot
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
