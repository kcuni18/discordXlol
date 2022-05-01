from .core import execute, select
from . import summoner

async def create(tournamentCode: str, summoner_id: int, name: str = None):
	await execute('INSERT INTO lobby(tournamentCode, name, open, summoner_id_0) VALUES(:code, :name, :open, :summonner_id_0)',{
		'code': tournamentCode,
		'name': name,
		'summonner_id_0': summoner_id,
		'open': 1
	})

async def close(tournamentCode: str):
	await execute('UPDATE lobby SET open=:open WHERE tournamentCode=:code', {'code':tournamentCode, 'open':0})

async def get(tournamentCode: str):
	data = await select('SELECT * FROM lobby WHERE tournamentCode=:code', {'code':tournamentCode})
	if len(data) != 1:
		return None
	return data[0]

async def get_open_lobby_list(pattern: str = ""):
	data = await select('SELECT * FROM lobby WHERE open=:open and tournamentCode LIKE :pattern', {'open': 1, 'pattern': f"%{pattern}%" })
	return [ obj['tournamentCode'] for obj in data ]

SUCCESS = 0
SUMMONER_IS_PRESENT = 1
LOBBY_IS_FULL = 2
async def insert_summoner(tournamentCode: str, summoner_id: int):
	data = await get(tournamentCode)
	for i in range(0, 10):
		name = f'summoner_id_{i}'
		if data[name] == summoner_id:
			return SUMMONER_IS_PRESENT
	for i in range(0, 10):
		name = f'summoner_id_{i}'
		if data[name] == None:
			await execute(f'UPDATE lobby SET {name}=:summoner_id', {'summoner_id':summoner_id})
			return SUCCESS
	return LOBBY_IS_FULL
	
