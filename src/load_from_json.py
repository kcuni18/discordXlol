import asyncio, json, os

from lib import *

async def run():
	await init()

	# summoners
	with open('_out/summoners.json', 'r') as file:
		summoners_data = json.loads(file.read())
	
	for data in summoners_data:
		summoner_data = lol.summoner.get_by_puuid(data['puuid'])
		await db.summoner.register(summoner_data)
		await db.summoner.set_discord_id(summoner_data['name'], data['discord_id'])

	# matches
	with open('_out/matches.json', 'r') as file:
		match_ids = json.loads(file.read())
	
	for match_id in match_ids:
		match_info = lol.match.get_info(match_id)
		await db.match.record_from_api(match_info)

	await terminate()

if __name__ == '__main__':
	asyncio.run(run())
