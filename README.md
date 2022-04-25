# Discord bot

### Setup
Clone the repository to the location of your choice.
Create the following files:
- `api_key.txt` should contain the api key for [RIOT games api](https://developer.riotgames.com/).
- `bot_token.txt` should contain your bot token taken from the [discord api](https://discord.com/developers/applications).
- `guild_id_list.txt` should contain the ids of the servers(one in each line) where you want the bot to be used. To find the guild id of your server check the explanation on this [link](https://poshbot.readthedocs.io/en/latest/guides/backends/setup-discord-backend/#find-your-guild-id-server-id).
- `bot_owner_id_list.txt` should contain a list of discord user ids(on in each line) which are allowed to use admin commands.
- `setup_summoner.txt` should contain the name of a summoner which is to be used in the setup. Ideally this should be a summoner which has participated in most custom games and has played as little as possible matched games so that a lot of games get recorded.

Instead of the files you can also use environment variables. See `init.bat` or `init.sh` for details.

Next execute `setup.bat` on windows or `setup.sh` on linux, to setup a virtual environment, install dependencies and create a database with the latest 100 games of the summoner name present in `setup_summoner.txt`.

Finally to run the bot, execute `run.bat` on windows or `run.sh` on linux.

You can create a shortcut to `run.bat` or `run.sh` and put it into your startup programs folder to run the bot on startup.
