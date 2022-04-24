from http.client import HTTPException
from pydoc import describe
from urllib.error import HTTPError
from aiohttp import HttpVersion
import discord
import os

import cache
import db
import lol

import match
import summoner

###### CONFIG ######
bot_owner_id=int(os.environ['bot_owner_id'])
bot_token=os.environ['bot_token']
guild_id=os.environ['guild_id']
version=os.environ['version']


###### INIT ######
bot = discord.Bot()

async def init():
	await db.init()
	cache.init()

@bot.event
async def on_ready():
	await init()
	print(f"We have logged in as {bot.user}")

###### COMMANDS ######

async def list_names(ctx: discord.AutocompleteContext):
	return await db.summoner.get_name_list(ctx.value)

@bot.slash_command(guild_ids=[guild_id], description="Link discord user to summoner.")
async def link(ctx: discord.ApplicationContext, summoner_name: discord.Option(str, "A league of legends username.", autocomplete=list_names)):
	user = ctx.author

	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is not None:
		if summoner_data['name'] == summoner_name:
			return await ctx.respond(f'You are already linked with `{summoner_name}`.')
		else:
			return await ctx.respond(f'You are already linked with summoner `{summoner_data["name"]}`.')

	summoner_data = await db.summoner.get_by_name(summoner_name)
	if summoner_data is not None:
		if summoner_data['discord_id'] != None:
			other_user = await bot.fetch_user(summoner_data['discord_id'])
			return await ctx.respond(f'Summoner `{summoner_name}` is already linked to {other_user.mention}.')
	else:
		return await ctx.respond(f'Summoner `{summoner_name}` is not registered(does not exist in the database). Use /register to register the summoner.')

	await db.summoner.set_discord_user(summoner_name, user)
	await db.commit()

	return await ctx.respond(f"Linked successfully with `{summoner_name}`.")


@bot.slash_command(guild_ids=[guild_id], description="Find the user linked with a summoner.")
async def find_summoner(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "The user you want to find the summoner for.", default=None)):
	if user is None:
		user = ctx.author

	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is None:
		return await ctx.respond(f'User {user.mention} is not linked.')

	return await ctx.respond(f'Linked summoner of {user.mention} is `{summoner_data["name"]}`.')

@bot.slash_command(guild_ids=[guild_id], description="Find the summoner linked with a user.")
async def find_user(ctx: discord.ApplicationContext, summoner_name: discord.Option(str, "A league of legends username.", autocomplete=list_names)):
	summoner_data = await db.summoner.get_by_name(summoner_name)
	if summoner_data is None:
		return await ctx.respond(f'Summoner `{summoner_name}` is not registered(does not exist in the database). Use /register to register the summoner.')
	if summoner_data['discord_id'] is None:
		return await ctx.respond(f'Summoner `{summoner_name}` is not linked to any user.')
	user = await bot.fetch_user(summoner_data['discord_id'])
	return await ctx.respond(f'Summoner `{summoner_name}` is linked to {user.mention}.')

@bot.slash_command(guild_ids=[guild_id], description="Unlink from summoner.")
async def unlink(ctx: discord.ApplicationContext):

	if not await db.summoner.is_registered_by_discord_user(ctx.author):
		return await ctx.respond(f"You are not linked to any summoner. Cannot unlink.")

	await db.execute('UPDATE summoner SET discord_id=:discord_id_new WHERE discord_id=:discord_id_old', {
		'discord_id_new': None,
		'discord_id_old': ctx.author.id
	})
	await db.commit()

	return await ctx.respond(f"Unlinked successfully.")

@bot.slash_command(guild_ids=[guild_id], description="Register a summoner.")
async def register(ctx: discord.ApplicationContext, summoner_name: discord.Option(str, "A league of legends username.")):
	if await db.summoner.is_registered_by_name(summoner_name):
		return await ctx.respond(f'Summoner `{summoner_name}` is already registered.')
	
	try:
		summoner_data = lol.summoner.get_by_name(summoner_name)
	except KeyError:
		return await ctx.respond(f'Summoner name `{summoner_name}` does not exist. Check your spelling.')
	except HTTPException as e:
		return await ctx.respond(f'Failed to retrieve `{summoner_name}` data. {str(e)}')
	
	await summoner.register(summoner_data)

	return await ctx.respond(f'Registered summoner `{summoner_name}` successfully.')


@bot.slash_command(guild_ids=[guild_id], description="Record matches.")
async def record_match(ctx: discord.ApplicationContext,
		user: discord.Option(discord.User, "One of the users who played in the custom game.", default=None),
		match_start: discord.Option(int, "The start index of custom games to be checked.", default=0, min_value=0, max_value=99),
		match_count: discord.Option(int, "The count of custom games to be checked.", default=1, min_value=1, max_value=100)):
	if user is None:
		user = ctx.author

	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is None:
		return await ctx.respond(f'User {user.mention} is not linked to any summoner.')

	await ctx.defer()
	match_ids = lol.match.get_id_list(summoner_data['puuid'], match_start, match_count)
	recorded_games = 0
	for match_id in match_ids:
		if (await db.match.is_recorded(match_id)):
			print("Match is already recorded. Skipping.")
		else:
			match_info = match.request_info(match_id)
			if match_info["info"]["gameType"] != "CUSTOM_GAME":
				print(f"Match type is {match_info['info']['gameType']}. Skipping.")
			elif match_info["info"]["gameMode"] != "CLASSIC":
				print(f"Match mode is {match_info['info']['gameMode']}. Skipping.")
			elif len(match_info["metadata"]["participants"]) != 10:
				print(f"Nr of participants is {len(match_info['metadata']['participants'])}. Skipping.")
			else:
				await match.record(match_info)
				recorded_games = recorded_games + 1
				print(f"Match {match_id} recorded.")
	return await ctx.followup.send(f"{match_count} {'game was' if match_count == 1 else 'games were'} checked. Of those {recorded_games} {'was' if recorded_games == 1 else 'were'} new and got recorded.")

@bot.slash_command(guild_ids=[guild_id], description="Find winrate of user.")
async def winrate(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "Tag of the user you want to find the winrate for.", default=None)):
	if user is None:
		user = ctx.author
	
	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is None:
		return await ctx.respond(f'User {user.mention} is not linked to any summoner.')

	wins = (await db.select('''
		SELECT COUNT(win) as count
		FROM participant
		JOIN summoner ON participant.summoner_id = summoner._id
		WHERE summoner._id=:id and participant.win == 1;
	''', {'id':summoner_data['_id']}))[0]['count']

	losses = (await db.select('''
		SELECT COUNT(win) as count
		FROM participant
		JOIN summoner ON participant.summoner_id = summoner._id
		WHERE summoner._id=:id and participant.win == 0;
	''', {'id':summoner_data['_id']}))[0]['count']

	if wins + losses == 0:
		return await ctx.respond(f"Summoner `{summoner_data['name']}` doesn't have any recorded games.")

	winrate = wins / (wins + losses) * 100
	await ctx.respond(f"Summoner `{summoner_data['name']}` has a winrate of {winrate:.2f}% with {wins} wins and {losses} losses.")

###### SHUTDOWN COMMAND ######
@bot.slash_command(guild_ids=[guild_id], description="Shuts down the bot. Only the owner of the bot can do so.")
async def shutdown(ctx: discord.ApplicationContext):
	if await bot.is_owner(ctx.author) or ctx.author.id == bot_owner_id:
		await ctx.respond('Logging out!')
		await terminate()
		await bot.close()
		bot.close()
	else:
		await ctx.respond('Only owner can shutdown the bot.')

async def terminate():
	await db.terminate()

###### RUN ######
if __name__ == '__main__':
	bot.run(bot_token)
