import requests
import json
import time

# global_variables
with open('api_key.txt', 'r') as file:
	api_key = file.read()

# request wrapper to retry after 10 seconds if failure
def _request_get(link):
	response = requests.get(link)
	while response.status_code != 200:
		print('Request failed. Status code {}.\n{}'.format(response.status_code, json.loads(response.text)["status"]["message"]))
		time.sleep(10)
		response = requests.get(link)
	return response


# api functions

# get match info from match id
def get_match_info(match_id):
	link = "https://europe.api.riotgames.com/lol/match/v5/matches/{}?api_key={}".format(match_id, api_key)
	return json.loads(_request_get(link).text)


# get match ids from summonner puuid
def get_match_ids(puuid, match_count=100):
	link = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?start=0&count={}&api_key={}".format(
		puuid, match_count, api_key)
	return json.loads(_request_get(link).text)


# get summoner info from puuid
def get_summoner_info_by_puuid(puuid):
	link = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{}?api_key={}".format(puuid, api_key)
	return json.loads(_request_get(link).text)


# get summoner info from name
def get_summoner_info_by_name(name):
	link = "https://eun1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(
		name.replace(" ", "%20"), api_key)
	return json.loads(_request_get(link).text)

if __name__ == '__main__':
	data = get_summoner_info_by_name('CapKunkka')
	print(json.dumps(data))
