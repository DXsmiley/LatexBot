> **This project has been halted in favour of [MathBot](https://github.com/DXsmiley/mathbot).** I will still look at and accept pull requests, however it is not under active development.

# Discord LaTeX Bot

This is a bot for [Discord](https://discordapp.com/) that automatically renders LaTeX formulas.

## Invocation

By default, the bot can be invoked with `!tex [latex code]`. Using `!help` or `!help tex` will private message the help.

Example: `!tex \sqrt{a^2 + b^2} = c`

## Running

To run the bot, you need [Python3](https://www.python.org/) and [discord.py](https://github.com/Rapptz/discord.py).

Running the bot for the first time will produce the `settings.json` file. You should edit this.

## Settings

### Login
You need either an email and passsword to login or a bot token. You can read more about that [here](https://discordapp.com/developers/docs/topics/oauth2#bot-vs-user-accounts)

If you're using an email and password, under "login_method", change "token" to "account"

Under "login", if you're using the account login method, change "email" and "password" to their respective value . If you're using a bot token, set "token" to be the token that discord auto generated for you.

### Channels

The list of servers and channels that the bot may access. The rules are as follows:
	
1. If the whitelist is empty, the bot may access all channels on all servers.
2. If the whitelist is not empty, the bot may access only the *servers* on the whitelist.
3. The bot may not access any *server* on the blacklist.
4. The bot may access any *channel* on the whitelist.
5. The bot may not access any *channel* on the blacklist.

Rules with larger numbers overrule the smaller ones.

### Renderer

`remote` will use an external server to render the LaTeX. **I do not own or maintain this server.**
Consider finding a different server. If too many people abuse it, it will be shut down.

`local` will attempt to use the programs `latex` and `dvipng` to render the LaTeX locally.
