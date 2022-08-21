import json
import requests
from http.client import HTTPException
from .. import config

cache_directory = "cache/ddragon"
version_file_path = "ddragon_versions.json"
lang = "en_GB"
region = config.data['lol']['region'].lower()

def get_json(link: str, params: dict = {}):
	response = requests.get(link, params=params)
	if response.status_code != 200:
		raise HTTPException(f"Request failed. Status code {response.status_code}.\n{response.text}")
	return json.loads(response.text)

def get_lastest_versions():
	# versions = get_json("https://ddragon.leagueoflegends.com/api/versions.json")
	return get_json(f"https://ddragon.leagueoflegends.com/realms/{region}.json")
