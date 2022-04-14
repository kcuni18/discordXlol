import discord

import league_api as lol
import database as db
import summoners
import matches
import util

def init():
	db.init()

def terminate():
	db.terminate()

def link_account(summoner_name: str, discord_user: discord.User):
	data = summoners.get_by_name(summoner_name)
	if data['discord_id'] != None:
		raise Exception(f'Summoner with name {summoner_name} is already linked to {discord_user.mention}.')
	
	data = db.select('SELECT * FROM summoner WHERE discord_id=:discord_id AND name!=:name', {'discord_id':discord_user.id, 'name':summoner_name})
	if len(data) == 1:
		raise Exception(f'You are already linked with account {data["name"]}')

	db.execute('UPDATE summoner SET discord_id=:discord_id WHERE name=:name', {
		'discord_id': discord_user.id,
		'name': summoner_name
	})

	db.commit()

def find_link(discord_user: discord.User):
	data = summoners.get_by_discord_user(discord_user)
	return data["name"]

def unlink_account(discord_user: discord.User):
	# check if user is registered
	summoners.get_by_discord_user(discord_user)

	db.execute('UPDATE summoner SET discord_id=:discord_id_new WHERE discord_id=:discord_id_old',{
		'discord_id_new': None,
		'discord_id_old': discord_user.id
	})
	db.commit()

def record_games(discord_user: discord.User, count: int = 1):
	
	summoner_data = summoners.get_by_discord_user(discord_user)
	match_ids = lol.get_match_ids(summoner_data["puuid"])

	recorded_count = 0
	failed_count = 0
	success_count = 0

	for match_id in match_ids:
		match_info = lol.get_match_info(match_id)
		match_id = util.match_id_to_int(match_id)

		if match_info["info"]["gameType"] != "CUSTOM_GAME":
			print(f"Match type is {match_info['info']['gameType']}. Skipping.")
		elif len(match_info["metadata"]["participants"]) != 10:
			print(f"Nr of participants is {len(match_info['metadata']['participants'])}. Skipping.")
		elif matches.is_recorded(match_id):
			print("Match is already recorded. Skipping.")
			recorded_count = recorded_count + 1
		else:
			# check all participants are registered
			for p in match_info["metadata"]["participants"]:
				data = db.select('SELECT name FROM summoner WHERE puuid=:puuid', {'puuid':p})
				if len(data) != 1:
					p_summoner_data = lol.get_summoner_info_by_puuid(p)
					db.execute('INSERT INTO summoner(puuid, name, profile_icon_id, level) VALUES(:puuid, :name, :profile_icon_id, :level);', {
						"puuid"				: p_summoner_data["puuid"],
						"name"				: p_summoner_data["name"],
						"profile_icon_id"	: p_summoner_data["profileIconId"],
						"level" 			: p_summoner_data["summonerLevel"]
					})
			db.commit()
			# insert match
			success, message = matches.record(match_info)
			if not success:
				print(f"Failed to insert match {match_id}. {message}")
				failed_count = failed_count + 1
			else:
				print(f"Inserted match successfully.")
				success_count = success_count + 1
		if count <= success_count + failed_count + recorded_count:
			break

	return success_count

def winrate(discord_user: discord.User):
	summoner_data = summoners.get_by_discord_user(discord_user)
	puuid = summoner_data['puuid']

	wins = db.select('''
		SELECT COUNT(match.blue_win) as count
		FROM summoner
		JOIN participant ON summoner.id = participant.summoner_id
		JOIN match ON participant.match_id = match.id
		WHERE summoner.puuid=:puuid and match.blue_win == participant.team;
	''', {'puuid':puuid})[0]['count']
	
	losses = db.select('''
		SELECT COUNT(match.blue_win) as count
		FROM summoner
		JOIN participant ON summoner.id = participant.summoner_id
		JOIN match ON participant.match_id = match.id
		WHERE summoner.puuid=:puuid and match.blue_win != participant.team;
	''', {'puuid':puuid})[0]['count']

	winrate = wins / (wins + losses) * 100

	return winrate, wins, losses

###### TESTING ######

if __name__ == '__main__':
	init()

	name = 'CapKunkka'
	summoner_data = lol.get_summoner_info_by_name(name)
	db.execute('INSERT INTO summoner(puuid, name, profile_icon_id, level) VALUES(:puuid, :name, :profile_icon_id, :level);', {
		"puuid"				: summoner_data["puuid"],
		"name"				: summoner_data["name"],
		"profile_icon_id"	: summoner_data["profileIconId"],
		"level" 			: summoner_data["summonerLevel"]
	})

	terminate()


