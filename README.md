# Discord bot

This discord bot records stats for inhouse league of legends games of a discord server.
Once added to the server you can record a certain ammount of those games and find certain
stats about them (only winrate for now).

### Setup
Clone the repository to the location of your choice.

Copy config_example.json to config.json and fill the data accordingly:
- `api_key` is the api key for [RIOT games api](https://developer.riotgames.com/).
- `region` is the game region where your games are to be played. This can be any of the following values: `BR`, `EUNE`, `EUW`, `JP`, `LAN`, `LAS`, `NA`, `OCE`, `RU`, `TR`
- `bot_token` is your bot token taken from the [discord api](https://discord.com/developers/applications).
- `guild_id_list` is a list of guild ids of the servers where you have added the bot. To find the guild id of your server check the explanation on this [link](https://poshbot.readthedocs.io/en/latest/guides/backends/setup-discord-backend/#find-your-guild-id-server-id).
- `owner_id_list` is a list of discord user ids which are allowed to use admin commands.

Next execute `scripts/setup.bat` on windows or `scripts/setup.sh` on linux, to setup a virtual environment and install dependencies.

Finally to run the bot, execute `scripts/run.bat` on windows or `scripts/run.sh` on linux.

You can create a shortcut to `scripts/run.bat` or `scripts/run.sh` and put it into your startup programs folder to run the bot on startup.
