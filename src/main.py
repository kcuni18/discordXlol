from http.client import HTTPException
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
async def winrate(ctx: discord.ApplicationContext,
	user: discord.Option(discord.User, "Tag of the user you want to find the winrate for.", default=None),
	_with: discord.Option(discord.User, "with", default=None),
	_vs: discord.Option(discord.User, "vs", default=None)):

	if user is None:
		user = ctx.author
	
	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is None:
		return await ctx.respond(f'User {user.mention} is not linked to any summoner.')

	if _with is not None:
		with_summoner_data = await db.summoner.get_by_discord_user(_with)
		if with_summoner_data is None:
			return await ctx.respond(f'User {_with.mention} is not linked to any summoner.')
	else:
		with_summoner_data = None

	if _vs is not None:
		vs_summoner_data = await db.summoner.get_by_discord_user(_vs)
		if vs_summoner_data is None:
			return await ctx.respond(f'User {_vs.mention} is not linked to any summoner.')
	else:
		vs_summoner_data = None

	wins = 0
	games = 0

	participants = (await db.select('''
		SELECT * FROM participant
		JOIN summoner ON participant.summoner_id = summoner._id
		WHERE summoner._id=:id
	''', {'id':summoner_data['_id']}))
	for participant in participants:
		match_id = participant['match_id']
		participant_teams = (await db.select('SELECT _id, team_id FROM participant_team WHERE match_id=:match_id', {'match_id':match_id}))
		
		friendly_participant_team = participant_teams[0] if participant_teams[0]['_id'] == participant['participant_team'] else participant_teams[1]
		ennemy_participant_team = participant_teams[0] if participant_teams[0]['_id'] != participant['participant_team'] else participant_teams[1]

		friendly_team = (await db.select('SELECT * FROM team WHERE _id=:team_id', {'team_id':friendly_participant_team['team_id']}))[0]
		ennemy_team = (await db.select('SELECT * FROM team WHERE _id=:team_id', {'team_id':ennemy_participant_team['team_id']}))[0]

		if with_summoner_data is not None:
			if with_summoner_data['_id'] not in db.team.dict_to_ids(friendly_team):
				continue
		if vs_summoner_data is not None:
			if vs_summoner_data['_id'] not in db.team.dict_to_ids(ennemy_team):
				continue
	
		wins = wins + participant['win']
		games = games + 1

	response = f"Summoner `{summoner_data['name']}` has played `{games}` {'match' if games == 1 else 'matches'}"
	if with_summoner_data is not None:
		response += f" with `{with_summoner_data['name']}`"
		if vs_summoner_data is not None:
			response += f" and against `{vs_summoner_data['name']}`"
	elif vs_summoner_data is not None:
		response += f" against `{vs_summoner_data['name']}`"
	if games != 0:
		response += f".\nOf those they have won `{wins}` and lost `{games - wins}` making a winrate of `{(wins / games * 100):.2f}%`."
	return await ctx.respond(response)

###### ADMIN COMMAND ######
@bot.slash_command(guild_ids=[guild_id], description="Link discord user to summoner.(Admin only)")
async def admin_link(ctx: discord.ApplicationContext,
		user: discord.Option(discord.User, "User to link."),
		summoner_name: discord.Option(str, "A league of legends username.", autocomplete=list_names)):
	if not (await bot.is_owner(ctx.author)) and ctx.author.id != bot_owner_id:
		return await ctx.respond(f"Only owner can use this command.")

	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is not None:
		if summoner_data['name'] == summoner_name:
			return await ctx.respond(f'User {user.mention} is already linked with `{summoner_name}`.')
		else:
			return await ctx.respond(f'User {user.mention} is already linked with summoner `{summoner_data["name"]}`.')

	summoner_data = await db.summoner.get_by_name(summoner_name)
	if summoner_data is not None:
		if summoner_data['discord_id'] != None:
			other_user = await bot.fetch_user(summoner_data['discord_id'])
			return await ctx.respond(f'Summoner `{summoner_name}` is already linked to {other_user.mention}.')
	else:
		return await ctx.respond(f'Summoner `{summoner_name}` is not registered(does not exist in the database). Use /register to register the summoner.')

	await db.summoner.set_discord_user(summoner_name, user)
	await db.commit()

	return await ctx.respond(f"Linked successfully user {user.mention} with `{summoner_name}`.")

@bot.slash_command(guild_ids=[guild_id], description="Unlink user from summoner.(Admin only)")
async def admin_unlink(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "User to unlink.")):
	if not (await bot.is_owner(ctx.author)) and ctx.author.id != bot_owner_id:
		return await ctx.respond(f"Only owner can use this command.")

	if not await db.summoner.is_registered_by_discord_user(user):
		return await ctx.respond(f"User {user.mention} is not linked to any summoner. Cannot unlink.")

	await db.execute('UPDATE summoner SET discord_id=:discord_id_new WHERE discord_id=:discord_id_old', {
		'discord_id_new': None,
		'discord_id_old': user.id
	})
	await db.commit()

	return await ctx.respond(f"Successfully unlinked {user.mention}.")

@bot.slash_command(guild_ids=[guild_id], description="Shuts down the bot.(Admin only)")
async def admin_shutdown(ctx: discord.ApplicationContext):
	if await bot.is_owner(ctx.author) or ctx.author.id == bot_owner_id:
		await ctx.respond('Logging out!')
		await terminate()
		await bot.close()
	else:
		await ctx.respond('Only owner can shutdown the bot.')

async def terminate():
	await db.terminate()

###### RUN ######
if __name__ == '__main__':
	bot.run(bot_token)
