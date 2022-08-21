import json
import time
import requests
from http.client import HTTPException

from .. import config

api_key=config.data['lol']['api_key']

def get(link: str, params: dict = {}):
	params['api_key'] = api_key
	response = requests.get(link, params=params)
	while response.status_code == 429:
		retry_time = int(response.headers.get('Retry-After'))
		print(f"{json.dumps(response.text)} Retrying in {retry_time} seconds.")
		time.sleep(retry_time + 1)
		response = requests.get(link, params=params)
	if response.status_code != 200:
		raise HTTPException(f"Request failed. Status code {response.status_code}.\n{response.text}")
	return json.loads(response.text)

def post(link: str, params: dict = {}, data: dict = {}):
	params['api_key'] = api_key
	response = requests.post(link, params=params, data=json.dumps(data))
	while response.status_code == 429:
		retry_time = int(response.headers.get('Retry-After'))
		print(f"{json.dumps(response.text)} Retrying in {retry_time} seconds.")
		time.sleep(retry_time + 1)
		response = requests.post(link, params=params, data=json.dumps(data))
	if response.status_code != 200:
		raise HTTPException(f"Request failed. Status code {response.status_code}.\n{response.text}")
	return json.loads(response.text)

def put(link: str, params: dict = {}, data: dict = {}):
	params['api_key'] = api_key
	response = requests.put(link, params=params, data=json.dumps(data))
	while response.status_code == 429:
		retry_time = int(response.headers.get('Retry-After'))
		print(f"{json.dumps(response.text)} Retrying in {retry_time} seconds.")
		time.sleep(retry_time + 1)
		response = requests.put(link, params=params, data=json.dumps(data))
	if response.status_code != 200:
		raise HTTPException(f"Request failed. Status code {response.status_code}.\n{response.text}")
	return json.loads(response.text)
