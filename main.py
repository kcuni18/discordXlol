import discord
import core as lol
import os

client = discord.Client()


def tag(user_id):
    return "<@{}>".format(user_id)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print("Bot is Online!\nCurrently operating: {0.user}".format(client))
    lol.init()


@client.event
async def on_message(message):
    print(message.author.id)
    if message.author == client.user:
        return

    if message.content.startswith("-") and message.author.id != 867140620870484039 and message.author.id != 454387076838850561: #and message.author.id == 104302118764023808
        temp = message.content.split("-")
        temp = temp[1].split(" ", 1)
        print(temp)
        if temp[0] == "tagme":
            await message.channel.send(tag(message.author.id))
        elif temp[0] == "record":
            attributes = temp[1].rsplit(" ", 1)
            await message.channel.send("`Will record games uvuvu`")
            await message.channel.send(lol.record_games(attributes[0], attributes[1]))
        elif temp[0] == "bestteam":
            attributes = temp[1].split(" ")
            await message.channel.send(lol.winrate_for_best_teams(int(attributes[0]), int(attributes[1])))
        elif temp[0] == "winrate":
            if len(temp) == 1:
                await message.channel.send(lol.winrate_by_discord(message.author.id))
            else:
                await message.channel.send(lol.winrate_by_name(temp[1]))
        elif temp[0] == "team":
            players = temp[1].split(" ")
            if len(players) != 5:
                await message.channel.send("You need 5 players for a team")
                return
            else:
                for player in players:
                    if player[0:3] != "<@!":
                        await message.channel.send("You have to tag players using @ sign")
                        return
            for i in range(len(players)):
                players[i] = int(players[i][3:21])
            print(players)
            await message.channel.send(lol.winrate_by_team(players))
        elif temp[0] == "help":
            await message.channel.send("`-record \"Summoner Name\" \"Number of games\"\nExample: -record Legit IRL 3\tWill record last 3 custom games from Legit IRL\"\n\n")
            await message.channel.send("-winrate \"Summoner Name\"\nExample: -winrate Takeshi Yuudai 3\tWill show 0% sepse hideki never wins uvuvu\n\n")
            await message.channel.send("-team \"numer ose \'all\'\" \nExample: -team 2\tTop 2 teams me highest winrate\n Example2: -team all \t tgjith teamsat`\"\n\n")
        elif temp[0] == "hesht":
            #await message.channel.send("/mute type: Voice user:%s time:1000" % tag(316496607564529666))
            pass

        if temp[0] == "mylink":
            await message.channel.send(lol.find_account(message.author.id))
        if temp[0] == "findlink":

            await message.channel.send(lol.find_account(int(temp[1][3:21])))

        if temp[0] == "link":
            await message.channel.send(lol.link_account(message.author.id, temp[1]))
        if temp[0] == "unlink":
            await message.channel.send(lol.unlink_account(message.author.id))

client.run(os.environ["TOKEN"])
