from . import core
from .. import config

domain = "https://europe.api.riotgames.com"
match_id_prefix = config.settings['lol']['match_id_prefix']

def get_info(match_id: int) -> dict:
	link = f"{domain}/lol/match/v5/matches/{match_id_prefix}_{match_id}"
	match_info = core.get(link)
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
