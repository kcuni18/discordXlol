import lol_api.lol_api as lol_api

def get_info(match_id: int) -> dict:
	link = "https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
	params = {
		'match_id': f"EUN1_{match_id}"
	}
	match_info = lol_api.request(link, params)
	return match_info

def get_id_list(summoner_puuid: str, match_start: int = 0, match_count: int = 100) -> list:
	link = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={match_start}&count={match_count}&api_key={api_key}"
	params = {
		'puuid': summoner_puuid,
		'match_start': match_start,
		'match_count': match_count
	}
	string_list = lol_api.request(link, params)
	return [ int(string[5:]) for string in string_list ]
