import main as main

import lol_api as lol
import cache
import db

import summoner
import match

import asyncio
import os

async def record_games(_summoner_data, start, count):
	match_ids = lol.match_get_id_list(_summoner_data['puuid'], start, count)

	ctr = 0
	for match_id in match_ids:
		if (await db.match_is_recorded(match_id)):
			print(f"{_summoner_data['name']}, {ctr}: Match is already recorded. Skipping.")
		else:
			try:
				match_info = match.request_info(match_id)
				if match_info["info"]["gameType"] != "CUSTOM_GAME":
					print(f"{_summoner_data['name']}, {ctr}: Match type is {match_info['info']['gameType']}. Skipping.")
				elif match_info["info"]["gameMode"] != "CLASSIC":
					print(f"{_summoner_data['name']}, {ctr}: Match mode is {match_info['info']['gameMode']}. Skipping.")
				elif len(match_info["metadata"]["participants"]) != 10:
					print(f"{_summoner_data['name']}, {ctr}: Nr of participants is {len(match_info['metadata']['participants'])}. Skipping.")
				else:
					summoner_datas = []
					for puuid in match_info["metadata"]["participants"]:
						try:
							await db.summoner_get_by_puuid(puuid)
						except KeyError:
							summoner_data = summoner.request_info(puuid)
							summoner_datas.append(summoner_data)
							await summoner.register(summoner_data)

					await match.record(match_info)
					print(f"{_summoner_data['name']}, {ctr}: Match {match_id} recorded.")

			except KeyError as e:
				print(f"{_summoner_data['name']}, {ctr}: Match {match_id} not found. {str(e)}")
			
		ctr = ctr + 1

async def run():
	await main.init()

	name = os.environ['setup_summoner']
	if not (await db.summoner_is_registered(name)):
		summoner_data = lol.summoner_get_by_name(name)
		await db.summoner_register(summoner_data)
	
	summoner_data = await db.summoner_get_by_name(name)

	await record_games(summoner_data, 0, 100)
	
	await db.commit()

	#data = await db.select("SELECT * FROM team")
	#print(data)

	names = (await db.summoner_get_name_list(""))
	print(f"registered summoners: {names}")

	await main.terminate()

if __name__ == '__main__':
	asyncio.run(run())

	
