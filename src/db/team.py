from .core import execute, select

async def get_by_ids(summoner_ids: list) -> dict:
	data = await select('''SELECT * FROM team WHERE
		summoner_id_0=:summoner_id_0 AND
		summoner_id_1=:summoner_id_1 AND
		summoner_id_2=:summoner_id_2 AND
		summoner_id_3=:summoner_id_3 AND
		summoner_id_4=:summoner_id_4''', ids_to_dict(summoner_ids))
	if len(data) != 1:
		return None
	return data[0]

async def is_registered_by_ids(summoner_ids: list) -> bool:
	data = await get_by_ids(summoner_ids)
	return data is not None

async def get_by_name(name: str):
	data = await select('SELECT * FROM team WHERE name:=name', {'name':name})
	if len(data) != 1:
		return None
	return data[0]

async def is_registered_by_name(name: str):
	data = await get_by_name(name)
	return data is not None

async def register(summoner_ids: list):
	await execute('''INSERT INTO team(summoner_id_0, summoner_id_1, summoner_id_2, summoner_id_3, summoner_id_4)
		VALUES(:summoner_id_0, :summoner_id_1, :summoner_id_2, :summoner_id_3, :summoner_id_4)''', ids_to_dict(summoner_ids))

async def set_name(summoner_ids: list, name: str):
	data = ids_to_dict(summoner_ids)
	data['name'] = name
	await execute('''UPDATE team SET name=:name WHERE
		summoner_id_0=:summoner_id_0 AND
		summoner_id_1=:summoner_id_1 AND
		summoner_id_2=:summoner_id_2 AND
		summoner_id_3=:summoner_id_3 AND
		summoner_id_4=:summoner_id_4''', data)

def ids_to_dict(summoner_ids: list) -> dict:
	summoner_ids.sort()
	return {
		'summoner_id_0': summoner_ids[0],
		'summoner_id_1': summoner_ids[1],
		'summoner_id_2': summoner_ids[2],
		'summoner_id_3': summoner_ids[3],
		'summoner_id_4': summoner_ids[4]
	}

def dict_to_ids(data: dict) -> list:
	return [
		data['summoner_id_0'],
		data['summoner_id_1'],
		data['summoner_id_2'],
		data['summoner_id_3'],
		data['summoner_id_4']
	]
