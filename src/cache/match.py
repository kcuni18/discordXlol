import os.path as path
import json

from .core import directory_matches

def get_info(id: int) -> dict:
	file_path = _file_path(id)
	with open(file_path) as file:
		json_data = json.loads(file.read())
	return json_data

def exists(id: int) -> bool:
	return path.isfile(_file_path(id))

def record(json_data: dict):
	match_id = json_data['info']['gameId']
	with open(_file_path(match_id), 'w') as file:
		file.write(json.dumps(json_data))

def _file_path(id: int):
	return f"{directory_matches}/{id}.json"
