import os
import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("Set DISCORD_TOKEN in your environment or .env file.")

intents = discord.Intents.default()

class System64Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

bot = System64Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.tree.command(name="sudo", description="Admin-only controlled message command")
@app_commands.describe(name="A display name/persona label", message="The message to send")
async def sudo(interaction: discord.Interaction, name: str, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You need Administrator permission to use /sudo.",
            ephemeral=True,
        )
        return

    if len(name) > 32 or len(message) > 2000:
        await interaction.response.send_message(
            "Name must be <= 32 characters and message <= 2000 characters.",
            ephemeral=True,
        )
        return

    embed = discord.Embed(description=message, color=discord.Color.blurple())
    embed.set_author(name=f"SUDO • {name}")
    embed.set_footer(text=f"Authorized by {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)
