from http.client import HTTPException
import requests
import json
import time
import os

# global_variables
api_key=os.environ['api_key']

# request wrapper to retry when request fails
def request(link: str, params: dict):
	params['api_key'] = api_key
	link = link.format(**params)
	response = requests.get(link)
	while response.status_code == 429:
		print(f"{json.dumps(json.loads(response.text)['status']['message'])} Retrying in {retry_time} seconds.")
		retry_time = int(response.headers.get('Retry-After'))
		time.sleep(retry_time + 1)
		response = requests.get(link)
	if response.status_code != 200:
		raise HTTPException(f"Request failed. Status code {response.status_code}.\n{json.loads(response.text)['status']['message']}")
	return json.loads(response.text)
