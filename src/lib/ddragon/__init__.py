import os, shutil
from .core import *

if not os.path.exists(cache_directory):
	os.makedirs(cache_directory)

version = None

def lookup_champions():
	return get_json(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/champion.json")

def lookup_items():
	return get_json(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/item.json")

def lookup_summoner_spells():
	return get_json(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/summoner.json")

def lookup_perks():
	return get_json(f"https://ddragon.leagueoflegends.com/cdn/{version}/data/{lang}/runesReforged.json")
