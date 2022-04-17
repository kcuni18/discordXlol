import discord
import os

import cache
import db
import lol_api

import match
import summoner

###### CONFIG ######
bot_owner_id=int(os.environ['bot_owner_id'])
bot_token=os.environ['bot_token']
guild_id=os.environ['guild_id']


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
	return await db.summoner_get_name_list(ctx.value)

@bot.slash_command(guild_ids=[guild_id], description="Link discord account summoner name.")
async def link(ctx: discord.ApplicationContext, summoner_name: discord.Option(str, "Your summoner name.", autocomplete=list_names)):
	user = ctx.author
	try:
		summoner_data = await db.summoner_get_by_discord_user(user)
		if summoner_data['name'] != summoner_name:
			await ctx.respond(f'You are already linked with account {summoner_data["name"]}')
			return
	except KeyError:
		pass
	try:
		summoner_data = await db.summoner_get_by_name(summoner_name)
		if summoner_data['discord_id'] != None:
			await ctx.respond(f'Summoner with name {summoner_name} is already linked to {user.mention}.')
			return
	
		await db.execute('UPDATE summoner SET discord_id=:discord_id WHERE name=:name', {
			'discord_id': user.id,
			'name': summoner_name
		})

		await db.commit()

		await ctx.respond(f"Linked successfully with `{summoner_name}`.")
		
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")


@bot.slash_command(guild_ids=[guild_id], description="Check whether your discord account is linked with a summoner.")
async def find_link(ctx: discord.ApplicationContext, user: discord.Option(discord.User, "The user you want to find the summoner name for.", default=None)):
	if user is None:
		user = ctx.author

	try:
		name = (await db.summoner_get_by_discord_user(user))['name']
		await ctx.respond(f'Linked account of {ctx.author.mention} is `{name}`.')
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")


@bot.slash_command(guild_ids=[guild_id], description="Unlink your discord account from your summoner.")
async def unlink(ctx: discord.ApplicationContext):
	try:
		await db.summoner_get_by_discord_user(ctx.author)

		await db.execute('UPDATE summoner SET discord_id=:discord_id_new WHERE discord_id=:discord_id_old', {
			'discord_id_new': None,
			'discord_id_old': ctx.author.id
		})
		await db.commit()

		await ctx.respond(f"Account unlinked successfully")
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")

@bot.slash_command(guild_ids=[guild_id], description="Record matches.")
async def record_match(ctx: discord.ApplicationContext,
		user: discord.Option(discord.User, "One of the users who played in the custom game.", default=None),
		match_start: discord.Option(int, "The start index of custom games to be checked.", default=0),
		match_count: discord.Option(int, "The count of custom games to be checked.", default=1)):
	if user is None:
		user = ctx.author
	await ctx.defer()

	try:
		summoner_data = await db.summoner_get_by_discord_user(user)
		match_ids = lol_api.match_get_id_list(summoner_data['puuid'], match_start, match_count)

		recorded_games = 0

		for match_id in match_ids:
			if (await db.match_is_recorded(match_id)):
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
					summoner_puuids = match_info["metadata"]["participants"]
					for puuid in summoner_puuids:
						try:
							await db.summoner_get_by_puuid(puuid)
						except KeyError:
							await summoner.register(summoner.request_info(puuid))
					await match.record(match_info)
					recorded_games = recorded_games + 1
					print(f"Match {match_id} recorded.")

		await ctx.followup.send(f"{match_count} {'game was' if match_count == 1 else 'games were'} checked. Of those {recorded_games} {'was' if recorded_games == 1 else 'were'} new and got recorded.")
	except Exception as e:
		await ctx.followup.send(f"Failed: {str(e)}")

@bot.slash_command(guild_ids=[guild_id], description="Find winrate of player.")
async def winrate(ctx: discord.ApplicationContext, player: discord.Option(discord.User, "Tag of the player you want to find the winrate for.", default=None)):
	if player is None:
		player = ctx.author
	try:
		summoner_data = await db.summoner_get_by_discord_user(player)
		puuid = summoner_data['puuid']

		wins = (await db.select('''
			SELECT COUNT(match.blue_win) as count
			FROM summoner
			JOIN participant ON summoner.id = participant.summoner_id
			JOIN match ON participant.match_id = match.id
			WHERE summoner.puuid=:puuid and match.blue_win != participant.team;
		''', {'puuid':puuid}))[0]['count']

		losses = (await db.select('''
			SELECT COUNT(match.blue_win) as count
			FROM summoner
			JOIN participant ON summoner.id = participant.summoner_id
			JOIN match ON participant.match_id = match.id
			WHERE summoner.puuid=:puuid and match.blue_win == participant.team;
		''', {'puuid':puuid}))[0]['count']

		winrate = wins / (wins + losses) * 100

		await ctx.respond(f"{(await db.summoner_get_by_discord_user(player))['name']} has a winrate of {winrate:.2f}% with {wins} wins and {losses} losses")
	except Exception as e:
		await ctx.respond(f"Failed: {str(e)}")

###### SHUTDOWN COMMAND ######
@bot.slash_command(guild_ids=[guild_id], description="Shuts down the bot.")
async def shutdown(ctx: discord.ApplicationContext):
	if await bot.is_owner(ctx.author) or ctx.author.id == bot_owner_id:
		await ctx.respond('Logging out!')
		await terminate()
		await ctx.bot.close()
	else:
		await ctx.respond('Only owner can shutdown the bot.')

async def terminate():
	await db.terminate()

###### RUN ######
if __name__ == '__main__':
	bot.run(bot_token)
