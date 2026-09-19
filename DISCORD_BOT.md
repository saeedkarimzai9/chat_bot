# Discord bot

This repository includes a lightweight Discord bot with safe, administrator-only controls.

## Commands

- `/ping` — checks that the bot is online and shows latency.
- `/about` — shows the bot's available commands.
- `/sudo name:Steve message:hello everyone` — sends a clearly labeled SUDO message.

The bot deliberately does not impersonate or send messages as another real Discord account. SUDO messages are labeled **SUDO • name** and include the administrator who authorized them.

## Local setup

1. Create a Discord application and bot in the Discord Developer Portal.
2. Invite it with the `bot` and `applications.commands` scopes.
3. Copy `.env.example` to `.env`.
4. Put your bot token in `DISCORD_TOKEN`.
5. Optional: put your Discord server ID in `DISCORD_GUILD_ID`. This makes slash-command updates appear in that server immediately while testing.
6. Install dependencies:

```powershell
python -m pip install -r requirements-discord.txt
```

7. Start the bot:

```powershell
python discord_bot.py
```

Never commit `.env` or expose the bot token.

## Permissions

Only members with the Discord **Administrator** permission can use `/sudo`.

The bot uses Discord slash commands and the default Discord gateway intents; it does not require privileged message-content access.
