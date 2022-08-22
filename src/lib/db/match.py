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
	data = await select(f'SELECT * FROM match WHERE id=:id', {'id':id})
	if len(data) != 1:
		return None
	return data

async def is_recorded(id: int):
	data = await get(id)
	if data == None:
		return False
	return True

async def record_from_replay(match_id: int, json_data: dict):
	await execute(insert_match_query, { "id": match_id, "gameLength": json_data['gameLength'] })

	summoner_ids = [ (await summoner.get_by_name(participant['NAME']))['_id'] for participant in json_data['statsJson'] ]
	teams_ids = [ summoner_ids[:5], summoner_ids[5:] ]

	for team_index, team_ids in enumerate(teams_ids):
		if not await team.is_registered_by_ids(team_ids):
			await team.register(team_ids)

		team_data = await team.get_by_ids(team_ids)

		team_participant_data = {
			'match_id': match_id,
			'team_id': team_data['_id'],
			'side': ['blue', 'red'][team_index],
			'win':  1 if json_data['statsJson'][team_index * 5] == "Win" else 0
		}
		await execute(insert_participant_team_query, team_participant_data)
		participant_team_id = (await select('SELECT _id FROM participant_team WHERE match_id=:match_id AND team_id=:team_id', team_participant_data))[0]['_id']

		for index, summoner_id in enumerate(team_ids):
			participant_data = json_data['statsJson'][index + team_index * 5].copy()

			participant_data['match_id'] = match_id
			participant_data['summoner_id'] = summoner_id
			participant_data['participant_team'] = participant_team_id
			participant_data['WIN'] = 1 if participant_data['WIN'] == 'Win' else 0
			participant_data['CHAMPION_ID'] = participant_data['SKIN']

			await execute(insert_participant_query, participant_data)


# out of date, might need in future
async def record_from_api(json_data: dict):
	match_id = json_data['info']['gameId']
	await execute(insert_match_query, { "id": match_id, "gameLength": json_data['info']['gameDuration']} )

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
			'win': json_data['info']['teams'][team_index]['win']
		}

		await execute(insert_participant_team_query, team_participant_data)
		participant_team_id = (await select('SELECT _id FROM participant_team WHERE match_id=:match_id AND team_id=:team_id', team_participant_data))[0]['_id']

		for summoner_id in team_ids:
			summoner_data = await summoner.get_by_id(summoner_id)
			index = json_data['metadata']['participants'].index(summoner_data['puuid'])
			participant_data = {
				'match_id': match_id,
				'summoner_id': summoner_id,
				'participant_team': participant_team_id,
				'ASSISTS': json_data['info']['participants'][index]['assists'],
				'BARON_KILLS': json_data['info']['participants'][index]['baronKills'],
				'BARRACKS_KILLED': json_data['info']['participants'][index]['inhibitorKills'],
				'BARRACKS_TAKEDOWNS': json_data['info']['participants'][index]['inhibitorTakedowns'],
				'BOUNTY_LEVEL': json_data['info']['participants'][index]['bountyLevel'],
				'CHAMPION_ID': json_data['info']['participants'][index]['championId'],
				'CHAMPION_TRANSFORM': json_data['info']['participants'][index]['championTransform'],
				'CHAMPIONS_KILLED': json_data['info']['participants'][index]['kills'],
				'CONSUMABLES_PURCHASED': json_data['info']['participants'][index]['consumablesPurchased'],
				'DOUBLE_KILLS': json_data['info']['participants'][index]['doubleKills'],
				'DRAGON_KILLS': json_data['info']['participants'][index]['dragonKills'],
				'EXP': json_data['info']['participants'][index]['champExperience'],
				'FRIENDLY_HQ_LOST': json_data['info']['participants'][index]['nexusLost'],
				'FRIENDLY_TURRET_LOST': json_data['info']['participants'][index]['turretsLost'],
				'GAME_ENDED_IN_EARLY_SURRENDER': json_data['info']['participants'][index]['gameEndedInEarlySurrender'],
				'GAME_ENDED_IN_SURRENDER': json_data['info']['participants'][index]['gameEndedInSurrender'],
				'GOLD_EARNED': json_data['info']['participants'][index]['goldEarned'],
				'GOLD_SPENT': json_data['info']['participants'][index]['goldSpent'],
				'HQ_KILLED': json_data['info']['participants'][index]['nexusKills'],
				'HQ_TAKEDOWNS': json_data['info']['participants'][index]['nexusTakedowns'],
				'INDIVIDUAL_POSITION': json_data['info']['participants'][index]['individualPosition'],
				'ITEM0': json_data['info']['participants'][index]['item0'],
				'ITEM1': json_data['info']['participants'][index]['item1'],
				'ITEM2': json_data['info']['participants'][index]['item2'],
				'ITEM3': json_data['info']['participants'][index]['item3'],
				'ITEM4': json_data['info']['participants'][index]['item4'],
				'ITEM5': json_data['info']['participants'][index]['item5'],
				'ITEM6': json_data['info']['participants'][index]['item6'],
				'ITEMS_PURCHASED': json_data['info']['participants'][index]['itemsPurchased'],
				'KILLING_SPREES': json_data['info']['participants'][index]['killingSprees'],
				'LARGEST_CRITICAL_STRIKE': json_data['info']['participants'][index]['largestCriticalStrike'],
				'LARGEST_KILLING_SPREE': json_data['info']['participants'][index]['largestKillingSpree'],
				'LARGEST_MULTI_KILL': json_data['info']['participants'][index]['largestMultiKill'],
				'LEVEL': json_data['info']['participants'][index]['champLevel'],
				'LONGEST_TIME_SPENT_LIVING': json_data['info']['participants'][index]['longestTimeSpentLiving'],
				'MAGIC_DAMAGE_DEALT_PLAYER': json_data['info']['participants'][index]['magicDamageDealt'],
				'MAGIC_DAMAGE_DEALT_TO_CHAMPIONS': json_data['info']['participants'][index]['magicDamageDealtToChampions'],
				'MAGIC_DAMAGE_TAKEN': json_data['info']['participants'][index]['magicDamageTaken'],
				'MINIONS_KILLED': json_data['info']['participants'][index]['totalMinionsKilled'],
				'NEUTRAL_MINIONS_KILLED': json_data['info']['participants'][index]['neutralMinionsKilled'],
				'NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE': json_data['info']['participants'][index]['challenges']['enemyJungleMonsterKills'],
				'NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE': json_data['info']['participants'][index]['challenges']['alliedJungleMonsterKills'],
				'NUM_DEATHS': json_data['info']['participants'][index]['deaths'],
				'OBJECTIVES_STOLEN': json_data['info']['participants'][index]['objectivesStolen'],
				'OBJECTIVES_STOLEN_ASSISTS': json_data['info']['participants'][index]['objectivesStolenAssists'],
				'PENTA_KILLS': json_data['info']['participants'][index]['pentaKills'],
				'PERK0': 		json_data['info']['participants'][index]['perks']['styles'][0]["selections"][0]["perk"],
				'PERK0_VAR1': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][0]["var1"],
				'PERK0_VAR2': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][0]["var2"],
				'PERK0_VAR3': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][0]["var3"],
				'PERK1':		json_data['info']['participants'][index]['perks']['styles'][0]["selections"][1]["perk"],
				'PERK1_VAR1':	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][1]["var1"],
				'PERK1_VAR2':	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][1]["var2"],
				'PERK1_VAR3':	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][1]["var3"],
				'PERK2': 		json_data['info']['participants'][index]['perks']['styles'][0]["selections"][2]["perk"],
				'PERK2_VAR1': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][2]["var1"],
				'PERK2_VAR2': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][2]["var2"],
				'PERK2_VAR3': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][2]["var3"],
				'PERK3': 		json_data['info']['participants'][index]['perks']['styles'][0]["selections"][3]["perk"],
				'PERK3_VAR1': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][3]["var1"],
				'PERK3_VAR2': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][3]["var2"],
				'PERK3_VAR3': 	json_data['info']['participants'][index]['perks']['styles'][0]["selections"][3]["var3"],
				'PERK4': 		json_data['info']['participants'][index]['perks']['styles'][1]["selections"][0]["perk"],
				'PERK4_VAR1': 	json_data['info']['participants'][index]['perks']['styles'][1]["selections"][0]["var1"],
				'PERK4_VAR2': 	json_data['info']['participants'][index]['perks']['styles'][1]["selections"][0]["var2"],
				'PERK4_VAR3': 	json_data['info']['participants'][index]['perks']['styles'][1]["selections"][0]["var3"],
				'PERK5': 		json_data['info']['participants'][index]['perks']['styles'][1]["selections"][1]["perk"],
				'PERK5_VAR1': 	json_data['info']['participants'][index]['perks']['styles'][1]["selections"][1]["var1"],
				'PERK5_VAR2': 	json_data['info']['participants'][index]['perks']['styles'][1]["selections"][1]["var2"],
				'PERK5_VAR3': 	json_data['info']['participants'][index]['perks']['styles'][1]["selections"][1]["var3"],
				'PERK_PRIMARY_STYLE': json_data['info']['participants'][index]['perks']['styles'][0]["style"],
				'PERK_SUB_STYLE': json_data['info']['participants'][index]['perks']['styles'][1]["style"],
				'STAT_PERK_0': json_data['info']['participants'][index]['perks']['statPerks']["offense"],
				'STAT_PERK_1': json_data['info']['participants'][index]['perks']['statPerks']["flex"],
				'STAT_PERK_2': json_data['info']['participants'][index]['perks']['statPerks']["defense"],
				'PHYSICAL_DAMAGE_DEALT_PLAYER': json_data['info']['participants'][index]['physicalDamageDealt'],
				'PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS': json_data['info']['participants'][index]['physicalDamageDealtToChampions'],
				'PHYSICAL_DAMAGE_TAKEN': json_data['info']['participants'][index]['physicalDamageTaken'],
				'PLAYER_ROLE': json_data['info']['participants'][index]['role'],
				'QUADRA_KILLS': json_data['info']['participants'][index]['quadraKills'],
				'SIGHT_WARDS_BOUGHT_IN_GAME': json_data['info']['participants'][index]['sightWardsBoughtInGame'],
				'SPELL1_CAST': json_data['info']['participants'][index]['spell1Casts'],
				'SPELL2_CAST': json_data['info']['participants'][index]['spell2Casts'],
				'SPELL3_CAST': json_data['info']['participants'][index]['spell3Casts'],
				'SPELL4_CAST': json_data['info']['participants'][index]['spell4Casts'],
				'SUMMON_SPELL1_CAST': json_data['info']['participants'][index]['summoner1Casts'],
				'SUMMON_SPELL2_CAST': json_data['info']['participants'][index]['summoner2Casts'],
				'TEAM_EARLY_SURRENDERED': json_data['info']['participants'][index]['teamEarlySurrendered'],
				'TEAM_POSITION': json_data['info']['participants'][index]['teamPosition'],
				'TIME_CCING_OTHERS': json_data['info']['participants'][index]['timeCCingOthers'],
				'TIME_PLAYED': json_data['info']['participants'][index]['timePlayed'],
				'TOTAL_DAMAGE_DEALT': json_data['info']['participants'][index]['totalDamageDealt'],
				'TOTAL_DAMAGE_DEALT_TO_BUILDINGS': json_data['info']['participants'][index]['damageDealtToBuildings'],
				'TOTAL_DAMAGE_DEALT_TO_CHAMPIONS': json_data['info']['participants'][index]['totalDamageDealtToChampions'],
				'TOTAL_DAMAGE_DEALT_TO_OBJECTIVES': json_data['info']['participants'][index]['damageDealtToObjectives'],
				'TOTAL_DAMAGE_DEALT_TO_TURRETS': json_data['info']['participants'][index]['damageDealtToTurrets'],
				'TOTAL_DAMAGE_SELF_MITIGATED': json_data['info']['participants'][index]['damageSelfMitigated'],
				'TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES': json_data['info']['participants'][index]['totalDamageShieldedOnTeammates'],
				'TOTAL_DAMAGE_TAKEN': json_data['info']['participants'][index]['totalDamageTaken'],
				'TOTAL_HEAL': json_data['info']['participants'][index]['totalHeal'],
				'TOTAL_HEAL_ON_TEAMMATES': json_data['info']['participants'][index]['totalHealsOnTeammates'],
				'TOTAL_TIME_CROWD_CONTROL_DEALT': json_data['info']['participants'][index]['totalTimeCCDealt'],
				'TOTAL_TIME_SPENT_DEAD': json_data['info']['participants'][index]['totalTimeSpentDead'],
				'TOTAL_UNITS_HEALED': json_data['info']['participants'][index]['totalUnitsHealed'],
				'TRIPLE_KILLS': json_data['info']['participants'][index]['tripleKills'],
				'TRUE_DAMAGE_DEALT_PLAYER': json_data['info']['participants'][index]['trueDamageDealt'],
				'TRUE_DAMAGE_DEALT_TO_CHAMPIONS': json_data['info']['participants'][index]['trueDamageDealtToChampions'],
				'TRUE_DAMAGE_TAKEN': json_data['info']['participants'][index]['trueDamageTaken'],
				'TURRET_TAKEDOWNS': json_data['info']['participants'][index]['turretTakedowns'],
				'TURRETS_KILLED': json_data['info']['participants'][index]['turretKills'],
				'UNREAL_KILLS': json_data['info']['participants'][index]['unrealKills'],
				'VISION_SCORE': json_data['info']['participants'][index]['visionScore'],
				'VISION_WARDS_BOUGHT_IN_GAME': json_data['info']['participants'][index]['visionWardsBoughtInGame'],
				'WARD_KILLED': json_data['info']['participants'][index]['wardsKilled'],
				'WARD_PLACED': json_data['info']['participants'][index]['wardsPlaced'],
				'WARD_PLACED_DETECTOR': json_data['info']['participants'][index]['detectorWardsPlaced'],
				'WIN': json_data['info']['participants'][index]["win"]
			}

			await execute(insert_participant_query, participant_data)
