import discord
import os
from keep_alive import keep_alive
from discord.ext import commands

keep_alive()

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------------- Ticket System ----------------
class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📩 Mở ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        channel = await guild.create_text_channel(
            f"ticket-{interaction.user.name}", overwrites=overwrites
        )
        await channel.send(
            content=f"{interaction.user.mention} Chào bạn! Vui lòng mô tả vấn đề của bạn.",
            view=CloseTicketButton()
        )
        await interaction.response.send_message(
            f"✅ Ticket của bạn đã được tạo: {channel.mention}", ephemeral=True
        )

class CloseTicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Đóng ticket", style=discord.ButtonStyle.red)
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔒 Ticket sẽ bị đóng sau 3 giây...", ephemeral=True)
        await interaction.channel.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    embed = discord.Embed(
        title="🎫 Hỗ trợ nhanh",
        description="**Bạn cần hỗ trợ nhanh?**\nHãy tạo ticket bằng cách ấn vào nút bên dưới.",
        color=0x00ff99
    )
    await ctx.send(embed=embed, view=TicketButton())

# ---------------- Welcome Event ----------------
@bot.event
async def on_ready():
    print(f"✅ Bot đã online với tên: {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1405475221212893191)
    if channel:
        embed = discord.Embed(
            title="🎉 Chào mừng bạn đến với server!",
            description=f"Xin chào {member.mention}, chúc bạn vui vẻ tại **{member.guild.name}**!",
            color=0x00ff99
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1405475220936200274/1405780506670399591/cee3322b-b1de-41a4-94a9-4378fb0216fc.png")
        await channel.send(embed=embed)

# ---------------- Auto Reply Bank ----------------
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "bank" in message.content.lower():
        embed = discord.Embed(
            title="Thông tin thanh toán",
            description=(
                "**STK:** 040920088\n"
                "**Chủ Tài Khoản:** PHAM NHU Y\n"
                "**Ngân Hàng:** MB BANK\n"
                "**Nội Dung:** ClashMc + Ingame"
            ),
            color=0x00ff00
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/1405475220936200274/1405780445135900772/IMG_3505.jpg")
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

# ---------------- Admin Command ----------------
@bot.command()
@commands.has_permissions(administrator=True)
async def admin(ctx, *, message: str):
    await ctx.message.delete()
    embed = discord.Embed(description=message, color=0x00ff99)
    await ctx.send(embed=embed)

@admin.error
async def admin_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bạn không có quyền dùng lệnh này!")

# ---------------- Clear Messages ----------------
@bot.command()
@commands.has_permissions(manage_messages=True)
async def cleartn(ctx, amount: int):
    if amount < 1:
        await ctx.send("⚠ Vui lòng nhập số lượng lớn hơn 0.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Đã xóa {len(deleted)-1} tin nhắn.", delete_after=3)

@cleartn.error
async def cleartn_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Bạn không có quyền xóa tin nhắn!")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("⚠ Vui lòng nhập số lượng hợp lệ!")

# ---------------- Run Bot ----------------
bot.run(os.getenv("TOKEN"))
