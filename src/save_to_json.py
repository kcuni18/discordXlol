import asyncio, json, os
import json

from lib import *

async def run():
	await init()
	
	os.makedirs("_out")

	# summoners
	summoner_data = await db.select('SELECT name, discord_id, puuid FROM summoner')
	with open('_out/summoners.json', 'w') as file:
		file.write(json.dumps(summoner_data))
	
	# matches
	match_ids = [ obj['gameId'] for obj in (await db.select('SELECT gameId FROM match')) ]
	with open('_out/matches.json', 'w') as file:
		file.write(json.dumps(match_ids))

	await terminate()

if __name__ == '__main__':
	asyncio.run(run())
