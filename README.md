# Discord Bot

A clean restart of the Discord bot project.

## Command

### /sudo say
Administrator-only command that posts a clearly labeled SUDO message using a name/persona label you choose.

Example:

/sudo say name:Steve message:Hello everyone!

The bot does **not** impersonate or claim to be a real Discord user. Every message is visibly labeled as SUDO and includes the administrator who authorized it.

## Setup

1. Create a Discord application and bot.
2. Invite the bot with the `bot` and `applications.commands` scopes.
3. Copy `.env.example` to `.env`.
4. Put your bot token in `DISCORD_TOKEN`.
5. Install dependencies:

```powershell
python -m pip install -r requirements-discord.txt
```

6. Run:

```powershell
python discord_bot.py
```

Never commit your `.env` file or bot token.
