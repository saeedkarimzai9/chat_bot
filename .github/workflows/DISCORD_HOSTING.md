# Free Discord bot hosting with GitHub Actions

This repository can run the System 64 Discord bot on GitHub-hosted runners at no cost for a public repository, subject to GitHub Actions limits and runner time limits.

## One-time setup

1. Open the repository on GitHub.
2. Go to **Settings → Secrets and variables → Actions**.
3. Create a **New repository secret** named:
   `DISCORD_TOKEN`
4. Paste your Discord bot token into the secret value.
5. Never commit the token to the repository.

## Start the bot

Go to **Actions → Run System 64 Discord Bot → Run workflow**.

The workflow installs Python and the Discord dependencies and starts `discord_bot.py`.

## Important limitation

GitHub-hosted runners are not a permanent 24/7 server. A workflow run eventually stops because of runner/job limits. Start the workflow again when it stops.

This is intended as a $0 way to test and run the bot. A true always-on host may require a service with a free tier that meets your usage needs.

## Discord behavior

The bot provides the administrator-only `/sudo` command. It uses a clearly labeled SUDO message and does not pretend to be another real Discord account.
