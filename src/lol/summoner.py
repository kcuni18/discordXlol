from . import core
from .. import config

domain_name = config.settings['lol']['match_id_prefix'].lower()
domain = f"https://{domain_name}.api.riotgames.com"

def get_by_puuid(puuid: str) -> dict:
	link = f"{domain}/lol/summoner/v4/summoners/by-puuid/{puuid}"
	summoner_data = core.get(link)
	return summoner_data

def get_by_name(name: str) -> dict:
	link = f"{domain}/lol/summoner/v4/summoners/by-name/{name}"
	summoner_data = core.get(link)
	return summoner_data
