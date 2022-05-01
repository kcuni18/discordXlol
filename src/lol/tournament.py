from . import core
from .. import config

import os

domain = "https://americas.api.riotgames.com"
tournament_api = config.settings['lol']['tournament_api']

def gen_provider():
	return core.post(f"{domain}/lol/{tournament_api}/v4/providers", data = {"region": config.settings['lol']['game_region'],"url": config.settings['lol']['tournament_callback_url']})

def gen_id():
	return core.post(f"{domain}/lol/{tournament_api}/v4/tournaments", data = {'providerId': provider_id})

# pickType: BLIND_PICK, DRAFT_MODE, ALL_RANDOM, TOURNAMENT_DRAFT
# mapType: SUMMONERS_RIFT, TWISTED_TREELINE, HOWLING_ABYSS
# spectatorType: NONE, LOBBYONLY, ALL
def gen_codes(mapType: str = "SUMMONERS_RIFT", pickType: str = "TOURNAMENT_DRAFT", spectatorType: str = "LOBBYONLY", count: int = 1):
	return core.post(f"{domain}/lol/{tournament_api}/v4/codes",
		params={'count':count, 'tournamentId': tournament_id},
		data={"mapType": mapType,"pickType": pickType,"spectatorType": spectatorType,"teamSize": 5})

import os

if not os.path.exists("provider_id.txt"):
	provider_id = gen_provider()
	with open("provider_id.txt", 'w') as file:
		file.write(str(provider_id))
else:
	with open("provider_id.txt", 'r') as file:
		provider_id = int(file.read())

if not os.path.exists("tournament_id.txt"):
	tournament_id = gen_id(provider_id)
	with open("tournament_id.txt", 'w') as file:
		file.write(str(tournament_id))
else:
	with open("tournament_id.txt", 'r') as file:
		tournament_id = int(file.read())
