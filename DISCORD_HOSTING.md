# Free Discord bot hosting with GitHub Actions

## One-time setup

1. Open the repository on GitHub.
2. Go to **Settings → Secrets and variables → Actions**.
3. Create a repository secret named `DISCORD_TOKEN` and paste your bot token into it.
4. Optional: create `DISCORD_GUILD_ID` with your Discord server ID. This gives that server fast slash-command synchronization.
5. Never commit the token to the repository.

## Start the bot

Go to **Actions → Run Discord Bot → Run workflow**.

The workflow installs Python and the Discord dependencies, then starts `discord_bot.py`.

The workflow is intentionally **manual** so normal GitHub pushes do not unexpectedly start a long-running bot process.

## Important limitation

GitHub-hosted runners are not permanent 24/7 Discord servers. A workflow run eventually stops because of runner/job limits. Start the workflow again when it stops.

This is intended as a $0 testing/run option.

## Discord behavior

The bot provides `/ping`, `/about`, and administrator-only `/sudo`. SUDO messages are clearly labeled and do not pretend to be another real Discord account.
