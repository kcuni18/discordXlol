import main as main

import lol_api as lol
import cache
import db

import summoner
import match

import asyncio

async def run():
	await main.init()

	name = 'CapKunkka'
	summoner_data = lol.summoner_get_by_name(name)
	await db.summoner_register(summoner_data)

	match_ids = lol.match_get_id_list(summoner_data['puuid'], 0, 20)
	for match_id in match_ids:
			if (await db.match_is_recorded(match_id)):
				print("Match is already recorded. Skipping.")
			else:
				match_info = match.request_info(match_id)
				if match_info["info"]["gameType"] != "CUSTOM_GAME":
					print(f"Match type is {match_info['info']['gameType']}. Skipping.")
				elif match_info["info"]["gameMode"] != "CLASSIC":
					print(f"Match mode is {match_info['info']['gameMode']}. Skipping.")
				elif len(match_info["metadata"]["participants"]) != 10:
					print(f"Nr of participants is {len(match_info['metadata']['participants'])}. Skipping.")
				else:
					summoner_puuids = match_info["metadata"]["participants"]
					for puuid in summoner_puuids:
						try:
							await db.summoner_get_by_puuid(puuid)
						except KeyError:
							await summoner.register(summoner.request_info(puuid))
					await match.record(match_info)
					print(f"Match {match_id} recorded.")
	await db.commit()

	#data = await db.select("SELECT * FROM team")
	#print(data)

	names = (await db.summoner_get_name_list(""))
	print(f"registered summoners: {names}")

	await main.terminate()

if __name__ == '__main__':
	asyncio.run(run())

	
