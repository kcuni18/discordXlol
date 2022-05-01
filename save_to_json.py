# v1.* -> v2.*

import asyncio
import json

from src import db

async def run():
	await db.init()
	
	# summoners
	summoner_data = await db.select('SELECT name, discord_id, puuid FROM summoner')
	with open('summoners.json', 'w') as file:
		file.write(json.dumps(summoner_data))
	
	# matches
	match_ids = [ obj['gameId'] for obj in (await db.select('SELECT gameId FROM match')) ]
	with open('matches.json', 'w') as file:
		file.write(json.dumps(match_ids))

	await db.terminate()

if __name__ == '__main__':
	asyncio.run(run())
