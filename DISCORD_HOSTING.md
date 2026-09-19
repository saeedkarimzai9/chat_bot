# Free Discord bot hosting with GitHub Actions

## One-time setup

1. Open the repository on GitHub.
2. Go to Settings -> Secrets and variables -> Actions.
3. Create a New repository secret named DISCORD_TOKEN.
4. Paste your Discord bot token into the secret value.
5. Never commit the token to the repository.

## Start the bot

Go to Actions -> Run System 64 Discord Bot -> Run workflow.

The workflow installs Python and the Discord dependencies and starts discord_bot.py.

## Important limitation

GitHub-hosted runners are not a permanent 24/7 server. A workflow run eventually stops because of runner/job limits. Start the workflow again when it stops.

This is intended as a $0 way to test and run the bot.

## Discord behavior

The bot provides the administrator-only /sudo command. It uses a clearly labeled SUDO message and does not pretend to be another real Discord account.