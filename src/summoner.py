import lol_api
import cache
import db

def request_info(puuid: str) -> dict:
	if cache.summoner_exists(puuid):
		return cache.summoner_get_info(puuid)
	else:
		return lol_api.summoner_get_by_puuid(puuid)

async def register(summoner_data: dict):
	puuid = summoner_data['puuid']
	if cache.summoner_exists(puuid):
		cache.summoner_register(summoner_data)
	if not (await db.summoner_is_registered(summoner_data['name'])):
		await db.summoner_register(summoner_data)
