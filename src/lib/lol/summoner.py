from . import core
from .. import config

import os
import json

domain_name = config.data['lol']['match_id_prefix'].lower()
domain = f"https://{domain_name}.api.riotgames.com"

cache_path = "cache/summoners"

if not os.path.isdir(cache_path):
	os.makedirs(cache_path)

def get_by_puuid(puuid: str) -> dict:
	# check cache
	cached_summoner_path = f"{cache_path}/{puuid}.json"
	if os.path.exists(cached_summoner_path):
		with open(cached_summoner_path) as file:
			summoner_data = json.loads(file.read())
	else:
		# request from riot api
		link = f"{domain}/lol/summoner/v4/summoners/by-puuid/{puuid}"
		summoner_data = core.get(link)

		# save in cache
		with open(cached_summoner_path) as file:
			file.write(json.dumps(summoner_data))

	return summoner_data

def get_by_name(name: str) -> dict:
	link = f"{domain}/lol/summoner/v4/summoners/by-name/{name}"
	summoner_data = core.get(link)
	return summoner_data
