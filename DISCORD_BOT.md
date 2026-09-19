# Discord SUDO bot

This adds an administrator-only `/sudo` slash command.

Usage:

`/sudo name:Steve message:hello everyone`

The bot deliberately does not impersonate or send messages as another real Discord account. It clearly labels the output as:

**SUDO • Steve**

and identifies the administrator who authorized it.

## Setup

1. Create a Discord application and bot in the Discord Developer Portal.
2. Put the bot token in a local `.env` file based on `.env.example`.
3. Invite the bot with the `bot` and `applications.commands` scopes.
4. Install dependencies:

```powershell
python -m pip install -r requirements-discord.txt
```

5. Start it:

```powershell
python discord_bot.py
```

Never commit `.env` or expose the bot token.
