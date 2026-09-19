import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set. Add it to your .env file or hosting secret.")

GUILD_ID = os.getenv("DISCORD_GUILD_ID")

intents = discord.Intents.default()


class System64Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        if GUILD_ID:
            guild = discord.Object(id=int(GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"Synced commands to test server {GUILD_ID}.")
        else:
            await self.tree.sync()
            print("Synced global slash commands.")


bot = System64Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.tree.command(name="ping", description="Check whether the bot is online.")
async def ping(interaction: discord.Interaction):
    latency_ms = round(bot.latency * 1000)
    await interaction.response.send_message(f"Pong! `{latency_ms}ms`")


@bot.tree.command(name="about", description="Show information about this Discord bot.")
async def about(interaction: discord.Interaction):
    embed = discord.Embed(
        title="System 64 Discord Bot",
        description="A lightweight Discord bot with an administrator-only SUDO command.",
        color=discord.Color.blurple(),
    )
    embed.add_field(name="/ping", value="Check bot latency.", inline=False)
    embed.add_field(name="/sudo", value="Send a clearly labeled admin-authorized message.", inline=False)
    embed.set_footer(text="System 64")
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="sudo", description="Admin-only controlled message command")
@app_commands.describe(
    name="A display name/persona label",
    message="The message to send",
)
async def sudo(interaction: discord.Interaction, name: str, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You need Administrator permission to use /sudo.",
            ephemeral=True,
        )
        return

    if len(name) > 32:
        await interaction.response.send_message(
            "The name must be 32 characters or fewer.",
            ephemeral=True,
        )
        return

    if len(message) > 2000:
        await interaction.response.send_message(
            "The message must be 2000 characters or fewer.",
            ephemeral=True,
        )
        return

    embed = discord.Embed(description=message, color=discord.Color.blurple())
    embed.set_author(name=f"SUDO • {name}")
    embed.set_footer(text=f"Authorized by {interaction.user.display_name}")
    await interaction.response.send_message(embed=embed)


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
):
    print(f"Command error: {error!r}")

    if interaction.response.is_done():
        await interaction.followup.send(
            "Something went wrong while running that command.",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            "Something went wrong while running that command.",
            ephemeral=True,
        )


bot.run(TOKEN)
