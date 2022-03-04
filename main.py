import core as lol
import os
from discord.ext import commands


# client = discord.Client()
bot = commands.Bot(command_prefix="-")


def tag(user_id):
    return "<@{}>".format(user_id)


@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))
    print('{} arguments: {}'.format(len(args), ', '.join(args)))


@bot.command()
async def tagme(ctx, *args):
    if len(args) == 0:
        await ctx.send(tag(ctx.author.id))
    else:
        await ctx.send(" ".join([tagged for tagged in args]))


@bot.command()
async def winrate(ctx, *args):
    if len(args) == 0:
        await ctx.send(lol.winrate_by_discord(ctx.author.id))
        return
    await ctx.send("\n".join(lol.winrate_by_discord(int(user[3:21])) for user in args))


@bot.command()
async def team(ctx, *args):
    players = []
    if len(args) != 5:
        ctx.send("You need 5 players for a team")
        return
    for player in args:
        if player[0:3] != "<@!":
            await ctx.send("You have to tag players using @ sign")
            return
    for i in range(len(args)):
        players.append(int(args[i][3:21]))
    reply = lol.winrate_by_team(players)
    print(type(reply))
    if str(type(reply)) == "<class 'list'>":
        await ctx.send(tag(reply[0]) + " is not linked!")
    else:
        await ctx.send(reply)


@bot.command()
async def bestteam(ctx, *args):
    await ctx.send(lol.winrate_for_best_teams(int(args[0]), int(args[1])))


@bot.command()
async def hesht(ctx, *args):
    pass


@bot.command()
async def findlink(ctx, *args):
    if len(args) == 0:
        await ctx.send(lol.find_account(ctx.author.id))
        return
    await ctx.send("\n".join(lol.find_account(int(user[3:21])) for user in args))


@bot.command()
async def mylink(ctx):
    await ctx.send(lol.find_account(ctx.author.id))


@bot.command()
async def unlink(ctx):
    await ctx.send(lol.unlink_account(ctx.author.id))


@bot.command()
async def link(ctx, *args):
    if len(args) == 0:
        await ctx.send("You must specify a name: -link Hidogu")
        return
    username = " ".join(word for word in args)
    await ctx.send(lol.link_account(ctx.author.id, username))


@bot.command()
async def record(ctx, *args):
    if len(args) == 1:
        await ctx.send(lol.record_games(ctx.author.id, int(args[0])))
        return
    await ctx.send(lol.record_games(int(args[0][3:21]), int(args[1])))

"""
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
"""

bot.run(os.environ["TOKEN"])
