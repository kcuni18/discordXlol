import lol_api
import cache
import db

def request_info(id: int) -> dict:
	if cache.match_exists(id):
		return cache.match_get_info(id)
	else:
		return lol_api.match_get_info(id)

async def record(json_data: dict):
	match_id = json_data['info']['gameId']
	if not cache.match_exists(match_id):
		cache.match_record(json_data)
	if not (await db.match_is_recorded(match_id)):
		await db.match_record(json_data)
