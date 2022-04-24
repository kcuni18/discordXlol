# v0.0.0 -> v1.0.*

import asyncio
import json

import db
import match
import summoner

async def run():
	await db.init()
	
	# summoners
	with open('summoners.json', 'r') as file:
		summoners_data = json.loads(file.read())
	
	for data in summoners_data:
		summoner_data = summoner.request_info(data['puuid'])
		await summoner.register(summoner_data)
		await db.summoner.set_discord_id(summoner_data['name'], data['discord_id'])

	# matches
	with open('matches.json', 'r') as file:
		match_ids = json.loads(file.read())
	
	for match_id in match_ids:
		match_info = match.request_info(match_id)
		await match.record(match_info)

	await db.terminate()

if __name__ == '__main__':
	asyncio.run(run())
