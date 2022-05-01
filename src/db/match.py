from .core import execute, select
from . import summoner
from . import team

with open('queries/insert_match.sql') as file:
	insert_match_query = file.read()
with open('queries/insert_participant.sql') as file:
	insert_participant_query = file.read()
with open('queries/insert_participant_team.sql') as file:
	insert_participant_team_query = file.read()


async def get(id: int):
	data = await select(f'SELECT * FROM match WHERE gameId=:id', {'id':id})
	if len(data) != 1:
		return None
	return data

async def is_recorded(id: int):
	data = await get(id)
	if data == None:
		return False
	return True

async def record(json_data: dict):

	match_id = json_data['info']['gameId']
	await execute(insert_match_query, json_data['info'])

	summoner_ids = [ (await summoner.get_by_puuid(data['puuid']))['_id'] for data in json_data["info"]["participants"]]
	teams_ids = [ summoner_ids[:5], summoner_ids[5:] ]

	for team_index, team_ids in enumerate(teams_ids):
		if not await team.is_registered_by_ids(team_ids):
			await team.register(team_ids)

		team_data = await team.get_by_ids(team_ids)

		team_participant_data = {
			'match_id': match_id,
			'side': ['blue', 'red'][team_index],
			'team_id': team_data['_id'],
			'baron_first': json_data['info']['teams'][team_index]['objectives']['baron']['first'],
			'baron_kills': json_data['info']['teams'][team_index]['objectives']['baron']['kills'],
			'champion_first': json_data['info']['teams'][team_index]['objectives']['champion']['first'],
			'champion_kills': json_data['info']['teams'][team_index]['objectives']['champion']['kills'],
			'dragon_first': json_data['info']['teams'][team_index]['objectives']['dragon']['first'],
			'dragon_kills': json_data['info']['teams'][team_index]['objectives']['dragon']['kills'],
			'inhibitor_first': json_data['info']['teams'][team_index]['objectives']['inhibitor']['first'],
			'inhibitor_kills': json_data['info']['teams'][team_index]['objectives']['inhibitor']['kills'],
			'rift_herald_first': json_data['info']['teams'][team_index]['objectives']['riftHerald']['first'],
			'rift_herald_kills': json_data['info']['teams'][team_index]['objectives']['riftHerald']['kills'],
			'tower_first': json_data['info']['teams'][team_index]['objectives']['tower']['first'],
			'tower_kills': json_data['info']['teams'][team_index]['objectives']['tower']['kills'],
			'win': json_data['info']['teams'][team_index]['win']
		}
		for i in range(0, len(json_data['info']['teams'][team_index]['bans'])):
			team_participant_data['ban_'+str(i)] = json_data['info']['teams'][team_index]['bans'][i]['championId']
		for i in range(len(json_data['info']['teams'][team_index]['bans']), 5):
			team_participant_data['ban_'+str(i)] = None

		await execute(insert_participant_team_query, team_participant_data)
		participant_team_id = (await select('SELECT _id FROM participant_team WHERE match_id=:match_id AND team_id=:team_id', team_participant_data))[0]['_id']

		for summoner_id in team_ids:
			summoner_data = await summoner.get_by_id(summoner_id)
			index = json_data['metadata']['participants'].index(summoner_data['puuid'])
			participant_data = json_data['info']['participants'][index].copy()

			participant_data['match_id'] = match_id
			participant_data['summoner_id'] = summoner_id
			participant_data['participant_team'] = participant_team_id

			participant_data['perk_defence'] = 		json_data['info']['participants'][index]['perks']['statPerks']['defense']
			participant_data['perk_flex'] = 		json_data['info']['participants'][index]['perks']['statPerks']['flex']
			participant_data['perk_offense'] = 		json_data['info']['participants'][index]['perks']['statPerks']['offense']
			participant_data['perk_style_primary_0'] = 		json_data['info']['participants'][index]['perks']['styles'][0]['selections'][0]['perk']
			participant_data['perk_style_primary_1'] = 		json_data['info']['participants'][index]['perks']['styles'][0]['selections'][1]['perk']
			participant_data['perk_style_primary_2'] = 		json_data['info']['participants'][index]['perks']['styles'][0]['selections'][2]['perk']
			participant_data['perk_style_primary_3'] = 		json_data['info']['participants'][index]['perks']['styles'][0]['selections'][3]['perk']
			participant_data['perk_style_secondary_0'] = 	json_data['info']['participants'][index]['perks']['styles'][1]['selections'][0]['perk']
			participant_data['perk_style_secondary_1'] = 	json_data['info']['participants'][index]['perks']['styles'][1]['selections'][1]['perk']

			await execute(insert_participant_query, participant_data)
