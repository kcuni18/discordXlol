from .core import execute, select
import discord

async def get_by_id(id: int) -> dict:
	data = await select('SELECT * FROM summoner WHERE _id=:id', {'id':id})
	if len(data) != 1:
		return None
	return data[0]

async def is_registered_by_id(id: int) -> bool:
	data = await get_by_id(id)
	return data is not None

async def get_by_name(name: str) -> dict:
	data = await select('SELECT * FROM summoner WHERE name=:name', {'name':name})
	if len(data) != 1:
		return None
	return data[0]

async def is_registered_by_name(name: str) -> bool:
	data = await get_by_name(name)
	return data is not None

async def get_by_discord_user(discord_user: discord.User) -> dict:
	data = await select('SELECT * FROM summoner WHERE discord_id=:discord_id', {'discord_id':discord_user.id})
	if len(data) != 1:
		return None
	return data[0]

async def is_registered_by_discord_user(discord_user: discord.User) -> bool:
	data = await get_by_discord_user(discord_user)
	return data is not None

async def get_by_puuid(puuid: str) -> dict:
	data = await select('SELECT * FROM summoner WHERE puuid=:puuid', {'puuid':puuid})
	if len(data) != 1:
		return None
	return data[0]

async def is_registered_by_puuid(puuid: str) -> bool:
	data = await get_by_puuid(puuid)
	return data is not None

async def get_name_list(string: str = "") -> list:
	string = "".join(["%", string, "%"])
	data = await select('SELECT name FROM summoner WHERE name LIKE :string', {'string':string})
	return [row['name'] for row in data]

async def set_discord_user(name: str, discord_user: discord.User):
	await execute('UPDATE summoner SET discord_id=:discord_id WHERE name=:name', {'name':name, 'discord_id':discord_user.id})

async def set_discord_id(name: str, discord_id: int):
	await execute('UPDATE summoner SET discord_id=:discord_id WHERE name=:name', {'name':name, 'discord_id':discord_id})

async def register(json_data: dict):
	await execute('INSERT INTO summoner(accountId, profileIconId, revisionDate, name, id, puuid, summonerLevel) VALUES(:accountId, :profileIconId, :revisionDate, :name, :id, :puuid, :summonerLevel);', json_data)
