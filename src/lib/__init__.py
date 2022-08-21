from . import config
from . import db
from . import lol
from . import ddragon

import os, shutil, json

async def init():
	# database init
	await db.init()
	if not await db.exists():
		# create database
		with open('queries/database.sql') as file:
			await db.executescript(file.read())

	# ddragon init
	new_versions = ddragon.get_lastest_versions()
	ddragon.version = new_versions['dd']

	# check ddragon versions
	if os.path.exists(ddragon.version_file_path):
		with open(ddragon.version_file_path, 'r') as file:
			versions = json.loads(file.read())

		if versions['dd'] != new_versions['dd']:
			shutil.rmtree(ddragon.cache_directory)
			os.makedirs(ddragon.cache_directory)
			with open(ddragon.version_file_path, 'w') as file:
				file.write(versions)
			
			# empty tables
			await db.execute("DELETE FROM champion;")
			await db.execute("DELETE FROM item;")
			await db.execute("DELETE FROM summoner_spell;")
			await db.execute("DELETE FROM perk;")
	else:
		with open(ddragon.version_file_path, 'w') as file:
			file.write(json.dumps(new_versions))
	
	# insert ddragon data
	if (await db.select("SELECT COUNT(*) as count FROM champion;"))[0]['count'] == 0:
		champion_data = ddragon.lookup_champions()
		for name, obj in champion_data['data'].items():
			await db.execute("INSERT INTO champion(id, name) VALUES(:id, :name);", { "id": int(obj["key"]), "name": name })

	if (await db.select("SELECT COUNT(*) as count FROM item;"))[0]['count'] == 0:
		item_data = ddragon.lookup_items()
		for id, obj in item_data['data'].items():
			await db.execute("INSERT INTO item(id, name) VALUES(:id, :name);", { "id": int(id), "name": obj['name'] })

	if (await db.select("SELECT COUNT(*) as count FROM summoner_spell;"))[0]['count'] == 0:
		summoner_spell_data = ddragon.lookup_summoner_spells()
		for id, obj in summoner_spell_data['data'].items():
			await db.execute("INSERT INTO summoner_spell(id, name) VALUES(:id, :name);", { "id": int(obj['key']), "name": obj['name'] })

	if (await db.select("SELECT COUNT(*) as count FROM perk;"))[0]['count'] == 0:
		perk_data = ddragon.lookup_perks()
		for perk_tree in perk_data:
			for row in perk_tree['slots']:
				for rune in row['runes']:
					await db.execute("INSERT INTO perk(id, name) VALUES(:id, :name);", { "id": rune['id'], "name": rune['name'] })

	await db.commit()


async def terminate():
	await db.terminate()