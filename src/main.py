from http.client import HTTPException
import discord

from lib import *
from lib.db.summoner import is_registered_by_name

###### CONFIG ######
bot_owner_id_list=config.data['discord']['owner_id_list']
guild_id_list=config.data['discord']['guild_id_list']
bot_token=config.data['discord']['bot_token']


###### INIT ######
bot = discord.Bot()

@bot.event
async def on_ready():
	await init()
	print(f"We have logged in as {bot.user}")

'''
@bot.event
async def on_message(message: discord.message.Message):
	if message.author == bot.user:
		return

	print(type(message))

	files = [await f.to_file() for f in message.attachments]
	print(f"atachment_count = {len(message.attachments)}")
	print(f"file_count = {len(files)}")
	for file in files:
		print(f"File content = `{str(file.fp.read())}`")
	
	print(f"message_content = `{message.content}`")

	if(message.content == "/record_match"):
		await message.channel.send("Match Recorded")
		'''

###### COMMANDS ######

async def list_names(ctx: discord.AutocompleteContext):
	return await db.summoner.get_name_list(ctx.value)

@bot.slash_command(guild_ids=guild_id_list, description="Link discord user to summoner.")
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


@bot.slash_command(guild_ids=guild_id_list, description="Find the user linked with a summoner.")
async def find_summoner(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "The user you want to find the summoner for.", default=None)):
	if user is None:
		user = ctx.author

	summoner_data = await db.summoner.get_by_discord_user(user)
	if summoner_data is None:
		return await ctx.respond(f'User {user.mention} is not linked.')

	return await ctx.respond(f'Linked summoner of {user.mention} is `{summoner_data["name"]}`.')

@bot.slash_command(guild_ids=guild_id_list, description="Find the summoner linked with a user.")
async def find_user(ctx: discord.ApplicationContext, summoner_name: discord.Option(str, "A league of legends username.", autocomplete=list_names)):
	summoner_data = await db.summoner.get_by_name(summoner_name)
	if summoner_data is None:
		return await ctx.respond(f'Summoner `{summoner_name}` is not registered(does not exist in the database). Use /register to register the summoner.')
	if summoner_data['discord_id'] is None:
		return await ctx.respond(f'Summoner `{summoner_name}` is not linked to any user.')
	user = await bot.fetch_user(summoner_data['discord_id'])
	return await ctx.respond(f'Summoner `{summoner_name}` is linked to {user.mention}.')

@bot.slash_command(guild_ids=guild_id_list, description="Unlink from summoner.")
async def unlink(ctx: discord.ApplicationContext):

	if not await db.summoner.is_registered_by_discord_user(ctx.author):
		return await ctx.respond(f"You are not linked to any summoner. Cannot unlink.")

	await db.execute('UPDATE summoner SET discord_id=:discord_id_new WHERE discord_id=:discord_id_old', {
		'discord_id_new': None,
		'discord_id_old': ctx.author.id
	})
	await db.commit()

	return await ctx.respond(f"Unlinked successfully.")

@bot.slash_command(guild_ids=guild_id_list, description="Register a summoner.")
async def register(ctx: discord.ApplicationContext, summoner_name: discord.Option(str, "A league of legends username.")):
	if await db.summoner.is_registered_by_name(summoner_name):
		return await ctx.respond(f'Summoner `{summoner_name}` is already registered.')
	
	try:
		summoner_data = lol.summoner.get_by_name(summoner_name)
	except KeyError:
		return await ctx.respond(f'Summoner name `{summoner_name}` does not exist. Check your spelling.')
	except HTTPException as e:
		return await ctx.respond(f'Failed to retrieve `{summoner_name}` data. {str(e)}')
	
	await db.summoner.register(summoner_data)

	return await ctx.respond(f'Registered summoner `{summoner_name}` successfully.')

import json

@bot.slash_command(guild_ids=guild_id_list, description="Record Matches.")
async def record_match(ctx: discord.ApplicationContext, attachment: discord.Option(discord.Attachment, "Json file extracted from a replay using roflToJson.py script")):
	match_id = int(attachment.filename[5:15])
	if await db.match.is_recorded(match_id):
		return await ctx.respond("Match is already recorded.")
	
	try:
		lol.match.get_info(match_id)
		return await ctx.respond("Match is not a custom game.")
	except:
		pass

	match_data = json.loads(await attachment.read())

	if len(match_data['statsJson']) != 10:
		return await ctx.respond("Match does not contain 10 players.")

	for obj in match_data['statsJson']:
		if not await db.summoner.is_registered_by_name(obj['NAME']):
			summoner_data = lol.summoner.get_by_name(obj['NAME'])
			await db.summoner.register(summoner_data)
	
	await db.match.record_from_replay(match_id, match_data)

	return await ctx.respond("Match recorded.")

# out of date, might need in future
#@bot.slash_command(guild_ids=guild_id_list, description="Record matches.")
#async def record_match(ctx: discord.ApplicationContext,
#		user: discord.Option(discord.User, "One of the users who played in the custom game.", default=None),
#		match_start: discord.Option(int, "The start index of custom games to be checked.", default=0, min_value=0, max_value=99),
#		match_count: discord.Option(int, "The count of custom games to be checked.", default=1, min_value=1, max_value=100),
#		match_id: discord.Option(int, "The id of the match.(All other options are ignored when using this one)", default=None)):
#
#	if match_id is not None:
#		if (await db.match.is_recorded(match_id)):
#			return await ctx.respond(f"Match `{match_id}` is already recorded. Skipping.")
#		else:
#			match_info = lol.match.get_info(match_id)
#			#if match_info["info"]["gameType"] != "CUSTOM_GAME":
#			#	return await ctx.respond(f"Match type of `{match_id}` is {match_info['info']['gameType']}.")
#			if match_info["info"]["gameMode"] != "CLASSIC":
#				return await ctx.respond(f"Match mode is {match_info['info']['gameMode']}. Skipping.")
#			elif len(match_info["metadata"]["participants"]) != 10:
#				return await ctx.respond(f"Nr of participants is {len(match_info['metadata']['participants'])}.")
#			else:
#				await db.match.record(match_info)
#				return await ctx.respond(f"Match with id `{match_id}` was recorded successfully.")
#
#	if user is None:
#		user = ctx.author
#
#	summoner_data = await db.summoner.get_by_discord_user(user)
#	if summoner_data is None:
#		return await ctx.respond(f'User {user.mention} is not linked to any summoner.')
#
#	await ctx.defer()
#	match_ids = lol.match.get_id_list(summoner_data['puuid'], match_start, match_count)
#	if len(match_ids) == 0:
#		return await ctx.followup.send(f"No matches were found for summoner `{summoner_data['name']}`.")
#	recorded_games = 0
#	for match_id in match_ids:
#		if (await db.match.is_recorded(match_id)):
#			print("Match is already recorded. Skipping.")
#		else:
#			match_info = lol.match.get_info(match_id)
#			#if match_info["info"]["gameType"] != "CUSTOM_GAME":
#			#	print(f"Match type is {match_info['info']['gameType']}. Skipping.")
#			if match_info["info"]["gameMode"] != "CLASSIC":
#				print(f"Match mode is {match_info['info']['gameMode']}. Skipping.")
#			elif len(match_info["metadata"]["participants"]) != 10:
#				print(f"Nr of participants is {len(match_info['metadata']['participants'])}. Skipping.")
#			else:
#				await db.match.record(match_info)
#				recorded_games = recorded_games + 1
#				print(f"Match {match_id} recorded.")
#	return await ctx.followup.send(f"{match_count} {'game was' if match_count == 1 else 'games were'} checked. Of those {recorded_games} {'was' if recorded_games == 1 else 'were'} new and got recorded.")


async def list_champions(ctx: discord.AutocompleteContext):
	return [ obj['name'] for obj in await db.select('SELECT name FROM champion WHERE name LIKE :pattern', {'pattern':'%'+ctx.value+'%'}) ]

role_list = ["JUNGLE", "MIDDLE", "TOP", "UTILITY", "SUPPORT", "BOTTOM", "ADC"]
async def list_roles(ctx: discord.AutocompleteContext):
	_list = []
	for role in role_list:
		if role.find(ctx.value) != -1:
			_list.append(role)
	return _list

@bot.slash_command(guild_ids=guild_id_list, description="Find winrate of user.")
async def winrate(ctx: discord.ApplicationContext,
	user: discord.Option(discord.User, "Tag of the user you want to find the winrate for.", default=None),
	_with: discord.Option(discord.User, "Ally of user.", default=None),
	_vs: discord.Option(discord.User, "Opponent of user.", default=None),
	champion_name: discord.Option(str, "Name of the champion played by the user", default=None, autocomplete=list_champions),
	role: discord.Option(str, "Role user played during the game.", default=None, autocomplete=list_roles)):

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

	if champion_name is not None:
		champion_data = (await db.select('SELECT * FROM champion WHERE name=:name', {'name':champion_name}))
		if len(champion_data) == 0:
			return await ctx.respond(f'Champion `{champion_name}` does not exist in the database.')
		else:
			champion_data = champion_data[0]
	else:
		champion_data = None

	if role is not None:
		if role == "SUPPORT":
			role_id = "UTILITY"
		elif role == "ADC":
			role_id = "BOTTOM"
		elif role in role_list:
			role_id = role
		else:
			return await ctx.respond(f'Role `{role}` is not a valid role.')
	else:
		role_id = None

	wins = 0
	games = 0

	participants = (await db.select('''
		SELECT * FROM participant
		JOIN summoner ON participant.summoner_id = summoner._id
		WHERE summoner._id=:id
	''', {'id':summoner_data['_id']}))

	for participant in participants:

		if champion_data is not None:
			if champion_data['id'] != participant['CHAMPION_ID']:
				continue
		
		if role_id is not None:
			if role_id != participant['TEAM_POSITION']:
				continue

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

		wins = wins + participant['WIN']
		games = games + 1

	response = f"Summoner `{summoner_data['name']}` has played `{games}` {'match' if games == 1 else 'matches'}"
	if role is not None:
		response += f" in the `{role}` position"
	if champion_data is not None:
		response += f" as `{champion_name}`"
	if with_summoner_data is not None:
		response += f" with `{with_summoner_data['name']}`"
		if vs_summoner_data is not None:
			response += f" and against `{vs_summoner_data['name']}`"
	elif vs_summoner_data is not None:
		response += f" against `{vs_summoner_data['name']}`"
	if games != 0:
		response += f".\nOf those they have won `{wins}` and lost `{games - wins}` making a winrate of `{(wins / games * 100):.2f}%`."
	return await ctx.respond(response)

###### ADMIN COMMANDS ######
admin_group = bot.create_group(name='admin', description='Admin commands.')

@admin_group.command(guild_ids=guild_id_list, name="link", description="Link discord user to summoner.(Admin only)")
async def admin_link(ctx: discord.ApplicationContext,
		user: discord.Option(discord.User, "User to link."),
		summoner_name: discord.Option(str, "A league of legends username.", autocomplete=list_names)):
	if not (await bot.is_owner(ctx.author)) and ctx.author.id not in bot_owner_id_list:
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

@admin_group.command(guild_ids=guild_id_list, name="unlink", description="Unlink user from summoner.(Admin only)")
async def admin_unlink(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "User to unlink.")):
	if not (await bot.is_owner(ctx.author)) and ctx.author.id not in bot_owner_id_list:
		return await ctx.respond(f"Only owner can use this command.")

	if not await db.summoner.is_registered_by_discord_user(user):
		return await ctx.respond(f"User {user.mention} is not linked to any summoner. Cannot unlink.")

	await db.execute('UPDATE summoner SET discord_id=:discord_id_new WHERE discord_id=:discord_id_old', {
		'discord_id_new': None,
		'discord_id_old': user.id
	})
	await db.commit()

	return await ctx.respond(f"Successfully unlinked {user.mention}.")

@admin_group.command(guild_ids=guild_id_list, name="shutdown", description="Shuts down the bot.(Admin only)")
async def admin_shutdown(ctx: discord.ApplicationContext):
	if await bot.is_owner(ctx.author) or ctx.author.id in bot_owner_id_list:
		await ctx.respond('Logging out!')
		await terminate()
		await bot.close()
	else:
		await ctx.respond('Only owner can shutdown the bot.')

###### RUN ######
if __name__ == '__main__':
	bot.run(bot_token)
