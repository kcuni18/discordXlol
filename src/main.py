import discord
import summoners

import core


###### CONFIG ######
with open('bot_token.txt') as file:
	bot_token = file.read()
with open('guild_id.txt') as file:
	guild_id = int(file.read())


###### INIT ######
core.init()
bot = discord.Bot()

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")


###### COMMANDS ######

@bot.slash_command(guild_ids=[guild_id], description="Link discord account summoner name.")
async def link(ctx: discord.ApplicationContext, name: discord.Option(str, "Your summoner name.")):
	try:
		core.link_account(name, ctx.author)
		await ctx.respond(f"Linked successfully with `{name}`.")
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")

@bot.slash_command(guild_ids=[guild_id], description="Check whether your discord account is linked with a summoner.")
async def find_link(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "The user you want to find the summoner name for.", default=None)):
	if user is None:
		user = ctx.author
	try:
		name = core.find_link(user)
		await ctx.respond(f'Linked account is `{name}`.')
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")


@bot.slash_command(guild_ids=[guild_id], description="Unlink your discord account from your summoner.")
async def unlink(ctx: discord.ApplicationContext):
	try:
		core.unlink_account(ctx.author)
		await ctx.respond(f"Account unlinked successfully")
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")

@bot.slash_command(guild_ids=[guild_id], description="Record a match.")
async def record_match(ctx: discord.ApplicationContext,
		user: discord.Option(discord.User, "One of the users who played in the custom game.", default=None),
		game_count: discord.Option(int, "The count of custom games to be checked.", default=1)):
	if user is None:
		user = ctx.author
	try:
		recorded_games = core.record_games(user, game_count)
		await ctx.respond(f"{game_count} {'game was' if game_count == 1 else 'games were'} checked. Of those {recorded_games} {'was' if recorded_games == 1 else 'were'} new and got recorded.")
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")

@bot.slash_command(guild_ids=[guild_id], description="Find winrate of player.")
async def winrate(ctx: discord.ApplicationContext, player: discord.Option(discord.User, "Tag of the player you want to find the winrate for.", default=None)):
	if player is None:
		player = ctx.author
	try:
		winrate, wins, losses = core.winrate(player)
		await ctx.respond(f"{summoners.get_by_discord_user(player)['name']} has a winrate of {winrate:.2f}% with {wins} wins and {losses} losses")
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")


###### SHUTDOWN COMMAND ######
@bot.slash_command(guild_ids=[guild_id], description="Shuts down the bot.")
async def shutdown(ctx: discord.ApplicationContext):
	if bot.is_owner(ctx.author):
		await ctx.respond('Logging out!')
		await bot.close()
	else:
		await ctx.respond('Only owner can shutdown the bot.')


###### TERMINATE ######
bot.run(bot_token)
core.terminate()
