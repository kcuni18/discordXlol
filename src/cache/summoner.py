import os.path as path
import json

from .core import directory_summoners

def get_info(puuid: str) -> dict:
	file_path = _file_path(puuid)
	with open(file_path) as file:
		json_data = json.loads(file.read())
	return json_data

def exists(puuid: str) -> bool:
	return path.isfile(_file_path(puuid))

def register(json_data: dict):
	puuid = json_data['puuid']
	with open(_file_path(puuid), 'w') as file:
		file.write(json.dumps(json_data))

def _file_path(puuid: str):
	return f"{directory_summoners}/{puuid}.json"
