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

    if message.content.startswith(
            "-") and message.author.id != 867140620870484039 and message.author.id != 454387076838850561:  # and message.author.id == 104302118764023808
        temp = message.content.split("-")
        temp = temp[1].split(" ", 1)
        # print(temp)
        if temp[0] == "tagme":
            await message.channel.send(tag(message.author.id))
        elif temp[0] == "record":
            attributes = temp[1].split(" ")
            print(attributes)
            if len(attributes) == 2:
                print(attributes[0][3:21], int(attributes[1]))
                await message.channel.send(lol.record_games(int(attributes[0][3:21]), int(attributes[1])))
            if len(attributes) == 1:
                await message.channel.send(lol.record_games(message.author.id, int(temp[1])))
        elif temp[0] == "bestteam":
            attributes = temp[1].split(" ")
            await message.channel.send(lol.winrate_for_best_teams(int(attributes[0]), int(attributes[1])))
        elif temp[0] == "winrate":
            if len(temp) == 1:
                await message.channel.send(lol.winrate_by_discord(message.author.id))
            else:
                await message.channel.send(lol.winrate_by_discord(int(temp[1][3:21])))
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
            reply = lol.winrate_by_team(players)
            print(reply)
            if len(reply) != 1:
                await message.channel.send(tag(reply[0]) + " is not linked!")
            else:
                await message.channel.send(message)
        elif temp[0] == "help":
            pass
        elif temp[0] == "hesht":
            # await message.channel.send("/mute type: Voice user:%s time:1000" % tag(316496607564529666))
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
