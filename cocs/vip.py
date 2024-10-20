import discord
from discord import Embed

# Variáveis de pagamento (PIX, QR Code)
qr_code_link = "https://cdn.discordapp.com/attachments/1291144028590706799/1296617719029960814/IMG_20240715_155531.jpg"
pix_code = "00020126550014br.gov.bcb.pix0114+55679810387370215DOACAO NOVA ERA5204000053039865802BR5924Willi Aparecido Oliveira6008Brasilia62090505v56ir63049489"
ticket_channel_id = "1262580157130997760"

# Link da imagem inicial para o comando !!comprarvip
image_link = "https://cdn.discordapp.com/attachments/1291144028590706799/1296634863176122399/DALLE_2024-10-17_21.20.39_-_A_survivor_in_a_post-apocalyptic_world_inside_a_dimly_lit_makeshift_shop._The_survivor_is_standing_at_a_counter_choosing_from_a_variety_of_weapons_f.jpg"

# Links das imagens para cada pacote VIP
image_diamante = "https://cdn.discordapp.com/attachments/1291144028590706799/1296639105022693486/DALLE_2024-10-17_22.00.36_-_A_scene_showing_a_person_in_a_post-apocalyptic_setting_opening_a_special_drop_box_labeled_Diamante_Caixa_de_Drop._The_box_has_a_metallic_futuristic.webp"
image_prata = "https://cdn.discordapp.com/attachments/1291144028590706799/1296636697085476915/DALLE_2024-10-17_21.50.02_-_A_scene_showing_a_person_in_a_post-apocalyptic_setting_opening_a_special_drop_box_labeled_Prata_Caixa_de_Drop._The_box_has_a_metallic_silver_appeara.webp"
image_bronze = "https://cdn.discordapp.com/attachments/1291144028590706799/1296636677770449007/DALLE_2024-10-17_21.50.38_-_A_scene_in_a_post-apocalyptic_environment_where_a_person_is_opening_a_special_drop_box_labeled_Bronze_Caixa_de_Drop._The_box_has_a_rugged_bronze-co.webp"

# Imagem das formas de pagamento
image_pagamento = "https://cdn.discordapp.com/attachments/1291144028590706799/1296644402248417331/DALLE_2024-10-17_22.20.45_-_A_post-apocalyptic_scene_showing_a_person_making_a_payment_at_a_high-tech_portal_with_a_sign_in_the_background_reading_Nova_Era._The_portal_has_glo.webp"

# Função para iniciar o processo de compra de VIP
async def comprar_vip(ctx, bot):
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

    message = await ctx.send(embed=embed)

    # Adicionar reações
    await message.add_reaction("💎")
    await message.add_reaction("🥈")
    await message.add_reaction("🥉")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["💎", "🥈", "🥉"] and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)

        await message.delete()

        if str(reaction.emoji) == "💎":
            await mostrar_detalhes(ctx, "DIAMANTE", 60, image_diamante, bot)
        elif str(reaction.emoji) == "🥈":
            await mostrar_detalhes(ctx, "PRATA", 30, image_prata, bot)
        elif str(reaction.emoji) == "🥉":
            await mostrar_detalhes(ctx, "BRONZE", 20, image_bronze, bot)

    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado!** Por favor, tente novamente.")

# Função para mostrar os detalhes de cada pacote VIP
async def mostrar_detalhes(ctx, pacote, valor, imagem, bot):
    # Definir descrições para cada pacote
    descricao = {
        "DIAMANTE": "💎 **Pacote DIAMANTE** 💎\n🔫 1 Sniper (Nível T6)...",
        "PRATA": "🥈 **Pacote PRATA** 🥈\n🪖 AK-47 (Nível T6)...",
        "BRONZE": "🥉 **Pacote BRONZE** 🥉\n⛏️ 1 Picareta de Ferro..."
    }

    embed = Embed(
        title=f"🔍 **Detalhes do Pacote {pacote}**",
        description=descricao[pacote],
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
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_option)

        await message.delete()

        if str(reaction.emoji) == "💲":
            await mostrar_pagamento(ctx, pacote, valor, bot)
        elif str(reaction.emoji) == "↩️":
            await comprar_vip(ctx, bot)

    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado!** Por favor, tente novamente.")

# Função para mostrar as opções de pagamento
async def mostrar_pagamento(ctx, pacote, valor, bot):
    embed = Embed(
        title=f"💳 **Pagamento do Pacote {pacote}** - R${valor}",
        description="Reaja para escolher uma das opções abaixo:\n"
                    "🖼️ - Ver **QR Code** para pagamento\n"
                    "📋 - Copiar **código PIX**\n"
                    "↩️ - Voltar para a lista de pacotes",
        color=discord.Color.gold()
    )
    embed.set_image(url=image_pagamento)
    message = await ctx.send(embed=embed)
    await message.add_reaction("🖼️")
    await message.add_reaction("📋")
    await message.add_reaction("↩️")

    def check_payment_option(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["🖼️", "📋", "↩️"] and reaction.message.id == message.id

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_payment_option)

        await message.delete()

        if str(reaction.emoji) == "🖼️":
            await enviar_qr_code(ctx)
        elif str(reaction.emoji) == "📋":
            await copiar_pix(ctx)
        elif str(reaction.emoji) == "↩️":
            await comprar_vip(ctx, bot)

    except Exception as e:
        await ctx.send("⏰ **Tempo esgotado!** Por favor, tente novamente.")

# Função para enviar o QR Code para pagamento
async def enviar_qr_code(ctx):
    embed = Embed(
        title="📲 **QR Code para Pagamento**",
        description="🔍 Escaneie o código abaixo para realizar o pagamento.",
        color=discord.Color.purple()
    )
    embed.set_image(url=qr_code_link)
    await ctx.send(embed=embed)

# Função para copiar o código PIX
async def copiar_pix(ctx):
    await ctx.send(f"📋 **Código PIX copiado:**\n```\n{pix_code}\n```")
    await ctx.send(f"Envie o comprovante no canal de tickets <#{ticket_channel_id}> após o pagamento.")
