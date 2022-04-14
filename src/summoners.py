import database as db
import discord

def get_by_name(name: str):
	data = db.select('SELECT * FROM summoner WHERE name=:name', {'name':name})
	if len(data) != 1:
		raise KeyError(f'Summoner name {name} is not registered.')
	return data[0]

def get_by_discord_user(discord_user: discord.User):
	data = db.select('SELECT * FROM summoner WHERE discord_id=:discord_id', {'discord_id':discord_user.id})
	if len(data) != 1:
		raise KeyError(f'User {discord_user.mention} is not linked to any summoner.')
	return data[0]

def get_by_puuid(puuid: str):
	data = db.select('SELECT * FROM summoner WHERE puuid=:puuid', {'puuid':puuid})
	if len(data) != 1:
		raise KeyError(f'Summoner with puuid {puuid} is not registered.')
	return data[0]

def get_name_list(string: str):
	data = db.select('SELECT name FROM summoner WHERE name LIKE :string', {'string':string})
	return [row['name'] for row in data]

def set_discord_user(name: str, discord_user: discord.User):
	db.execute('UPDATE summoner SET discord_id=:discord_id WHERE name=:name', {'name':name, 'discord_id':discord_user.id})

def is_registered(name: str):
	try:
		get_by_name(name)
		return True
	except KeyError:
		return False

def add(json_data: dict):
	db.execute('INSERT INTO summoner(puuid, name, profile_icon_id, level) VALUES(:puuid, :name, :profile_icon_id, :level);', {
		"puuid"				: json_data["puuid"],
		"name"				: json_data["name"],
		"profile_icon_id"	: json_data["profileIconId"],
		"level" 			: json_data["summonerLevel"]
	})


