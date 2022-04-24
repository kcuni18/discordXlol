from .core import request

def get_by_puuid(puuid: str) -> dict:
	link = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}"
	params = {
		'puuid': puuid
	}
	summoner_data = request(link, params)
	return summoner_data

def get_by_name(name: str) -> dict:
	link = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}?api_key={api_key}"
	params = {
		'name': name.replace(" ", "%20")
	}
	summoner_data = request(link, params)
	return summoner_data
