# Discord bot

This discord bot records stats for inhouse league of legends games of a discord server.
Once added to the server you can record a certain ammount of those games and find certain
stats about them (only winrate per summoner for now).

The bot is not functional right now.

### Setup
Clone the repository to the location of your choice.

Copy config_example.json to config.json and fill the data accordingly:
- `lol_api_key` is the api key for [RIOT games api](https://developer.riotgames.com/).
- `discord_bot_token` is your bot token taken from the [discord api](https://discord.com/developers/applications).
- `game_region` is the game region where your games are to be played. This can be any of the following values: `BR`, `EUNE`, `EUW`, `JP`, `LAN`, `LAS`, `NA`, `OCE`, `RU`, `TR`
- `tournament_api` should always be `tournament` unless you are in a testing environment in which case it should be `tournament-stub`
- `guild_id_list.txt` is a list of guild ids of the servers where you have added the bot. To find the guild id of your server check the explanation on this [link](https://poshbot.readthedocs.io/en/latest/guides/backends/setup-discord-backend/#find-your-guild-id-server-id).
- `owner_id_list` is a list of discord user ids which are allowed to use admin commands.
- `summoner` is the name of a summoner which is to be used in the setup. Ideally this should be a summoner which has participated in most previous inhouse games so that a lot of games get recorded.

Next execute `setup.bat` on windows or `setup.sh` on linux, to setup a virtual environment, install dependencies and create a database with the latest 100 games of the summoner name present in `setup_summoner.txt`.

Finally to run the bot, execute `run.bat` on windows or `run.sh` on linux.

You can create a shortcut to `run.bat` or `run.sh` and put it into your startup programs folder to run the bot on startup.
