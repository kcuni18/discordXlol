from . import lol
from . import cache
from . import db

def request_info(puuid: str) -> dict:
	if cache.summoner.exists(puuid):
		return cache.summoner.get_info(puuid)
	else:
		return lol.summoner.get_by_puuid(puuid)

async def register(summoner_data: dict):
	puuid = summoner_data['puuid']
	if not cache.summoner.exists(puuid):
		cache.summoner.register(summoner_data)
	if not (await db.summoner.is_registered_by_name(summoner_data['name'])):
		await db.summoner.register(summoner_data)
