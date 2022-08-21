from . import core
from .. import config

import os
import json

domain = "https://europe.api.riotgames.com"
match_id_prefix = config.data['lol']['match_id_prefix']

cache_path = "cache/matches"

if not os.path.isdir(cache_path):
	os.makedirs(cache_path)

def get_info(match_id: int) -> dict:
	# check cache
	cached_match_path = f"{cache_path}/{match_id}.json"
	if os.path.exists(cached_match_path):
		with open(cached_match_path) as file:
			match_info = json.loads(file.read())
	else:
		# request from riot api
		link = f"{domain}/lol/match/v5/matches/{match_id_prefix}_{match_id}"
		match_info = core.get(link)

		# save in cache
		with open(cached_match_path) as file:
			file.write(json.dumps(match_info))
	
	return match_info

# match_type : ranked, normal, tourney, tutorial
def get_id_list(summoner_puuid: str, match_start: int = 0, match_count: int = 20, match_type: str = "tourney") -> list:
	link = f"{domain}/lol/match/v5/matches/by-puuid/{summoner_puuid}/ids"
	params = {
		'type': match_type,
		'match_start': match_start,
		'match_count': match_count
	}
	if match_type is None:
		del params['type']
	string_list = core.get(link, params)
	return [ int(string[len(match_id_prefix) + 1:]) for string in string_list ]

def convert_to_db_match(match_info: dict):
	pass
