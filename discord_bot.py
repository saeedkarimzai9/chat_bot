import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set.")

intents = discord.Intents.default()


class System64Bot(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("Slash commands synced.")


bot = System64Bot()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")


@bot.tree.command(
    name="sudo",
    description="Send a clearly labeled SUDO message",
)
@app_commands.describe(
    name="The display name/persona label",
    message="The message to send",
)
async def sudo(
    interaction: discord.Interaction,
    name: str,
    message: str,
):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You need Administrator permission to use /sudo.",
            ephemeral=True,
        )
        return

    name = name.strip()
    message = message.strip()

    if not name:
        await interaction.response.send_message(
            "The name cannot be empty.",
            ephemeral=True,
        )
        return

    if not message:
        await interaction.response.send_message(
            "The message cannot be empty.",
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

    embed = discord.Embed(
        description=message,
        color=discord.Color.blurple(),
    )
    embed.set_author(name=f"SUDO • {name}")
    embed.set_footer(
        text=f"Authorized by {interaction.user.display_name}"
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction,
    error: app_commands.AppCommandError,
):
    print(f"Command error: {error!r}")

    if interaction.response.is_done():
        await interaction.followup.send(
            "The command could not be completed.",
            ephemeral=True,
        )
    else:
        await interaction.response.send_message(
            "The command could not be completed.",
            ephemeral=True,
        )


bot.run(TOKEN)
