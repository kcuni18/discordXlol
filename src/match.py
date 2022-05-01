from . import lol
from . import cache
from . import db

from . import summoner

def request_info(id: int) -> dict:
	if cache.match.exists(id):
		return cache.match.get_info(id)
	else:
		return lol.match.get_info(id)

async def record(json_data: dict):
	match_id = json_data['info']['gameId']
	if not cache.match.exists(match_id):
		cache.match.record(json_data)
	if not (await db.match.is_recorded(match_id)):
		for puuid in json_data["metadata"]["participants"]:
			if not (await db.summoner.is_registered_by_puuid(puuid)):
				summoner_data = summoner.request_info(puuid)
				await summoner.register(summoner_data)
		await db.match.record(json_data)
