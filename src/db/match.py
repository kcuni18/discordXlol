import db.database as db
import db.summoner as summoner

with open('src/queries/insert_match.sql') as file:
	insert_match_query = file.read()
with open('src/queries/insert_participant.sql') as file:
	insert_participant_query = file.read()

async def get(id: int):
	data = await db.select(f'SELECT * FROM match WHERE id=:id', {'id':id})
	if len(data) != 1:
		raise KeyError(f'Match {id} is not recorded.')
	return data

async def is_recorded(id: int):
	try:
		await get(id)
		return True
	except KeyError:
		return False

async def record(json_data: dict):

	summoner_ids = [ (await summoner.get_by_puuid(puuid))['id'] for puuid in json_data["metadata"]["participants"]]

	team_blue_bytes = team_ids_to_bytes(summoner_ids[0:5])
	team_red_bytes = team_ids_to_bytes(summoner_ids[5:10])

	await db.execute(insert_match_query, {
		'id' 		: json_data["info"]["gameId"],
		'start'		: json_data["info"]["gameCreation"],
		'duration' 	: json_data["info"]["gameDuration"],
		'name' 		: json_data["info"]["gameName"],
		'team_blue'	: team_blue_bytes,
		'team_red' 	: team_red_bytes,
		'blue_win' 	: 1 if json_data["info"]["participants"][0]["win"] else 0
	})

	for i in range(0, 10):
		summoner_id = (await summoner.get_by_puuid(json_data["metadata"]["participants"][i]))['id']
		participant_data = json_data["info"]["participants"][i]
		await db.execute(insert_participant_query, {
			'summoner_id' 			: summoner_id,
			'match_id' 				: json_data["info"]["gameId"],
			'team' 					: 0 if i < 5 else 1,
			'position'				: participant_data["teamPosition"],
			'kills' 				: participant_data["kills"],
			'assists' 				: participant_data["assists"],
			'deaths' 				: participant_data["deaths"],
			'double_kills' 			: participant_data["doubleKills"],
			'triple_kills' 			: participant_data["tripleKills"],
			'quadra_kills' 			: participant_data["quadraKills"],
			'penta_kills' 			: participant_data["pentaKills"],
			'total_minion_kills' 	: participant_data["totalMinionsKilled"],
			'gold_earned' 			: participant_data["goldEarned"],
			'gold_spent' 			: participant_data["goldSpent"],
			'total_damage_dealt' 					: participant_data["totalDamageDealt"],
			'total_damage_dealt_to_champions' 		: participant_data["totalDamageDealtToChampions"],
			'total_damage_shielded_on_teammates' 	: participant_data["totalDamageShieldedOnTeammates"],
			'total_damage_taken' 					: participant_data["totalDamageTaken"],
			'physical_damage_dealt' 				: participant_data["physicalDamageDealt"],
			'physical_damage_dealt_to_champions' 	: participant_data["physicalDamageDealtToChampions"],
			'physical_damage_taken' 				: participant_data["physicalDamageTaken"],
			'magic_damage_dealt' 					: participant_data["magicDamageDealt"],
			'magic_damage_dealt_to_champions' 		: participant_data["magicDamageDealtToChampions"],
			'magic_damage_taken' 					: participant_data["magicDamageTaken"],
			'true_damage_dealt' 					: participant_data["trueDamageDealt"],
			'true_damage_dealt_to_champions' 		: participant_data["trueDamageDealtToChampions"],
			'true_damage_taken' 					: participant_data["trueDamageTaken"],
			'total_heal' 							: participant_data["totalHeal"],
			'total_heal_on_teammates' 				: participant_data["totalHealsOnTeammates"],
			'self_mitigated_damage'					: participant_data["damageSelfMitigated"],
			'damage_dealt_to_turrets'				: participant_data["damageDealtToTurrets"],
			'damage_dealt_to_objectives'			: participant_data["damageDealtToObjectives"],
			'damage_dealt_to_buildings'				: participant_data["damageDealtToBuildings"],
			'time_ccing_others' 					: participant_data["timeCCingOthers"],
			'spell_1_casts' 		: participant_data["spell1Casts"],
			'spell_2_casts' 		: participant_data["spell2Casts"],
			'spell_3_casts' 		: participant_data["spell3Casts"],
			'spell_4_casts' 		: participant_data["spell4Casts"],
			'summoner_1_casts' 		: participant_data["summoner1Casts"],
			'summoner_1_id' 		: participant_data["summoner1Id"],
			'summoner_2_casts' 		: participant_data["summoner2Casts"],
			'summoner_2_id' 		: participant_data["summoner2Id"],
			'baron_kills' 			: participant_data["baronKills"],
			'turret_kills' 			: participant_data["turretKills"],
			'turret_takedowns' 		: participant_data["turretTakedowns"],
			'turrets_lost' 			: participant_data["turretsLost"],
			'bounty_level' 			: participant_data["bountyLevel"],
			'vision_score' 			: participant_data["visionScore"],
			'vision_wards_bought' 	: participant_data["visionWardsBoughtInGame"],
			'wards_killed' 			: participant_data["wardsKilled"],
			'wards_placed' 			: participant_data["wardsPlaced"],
			'champ_experience' 		: participant_data["champExperience"],
			'champ_level' 			: participant_data["champLevel"],
			'champ_id' 				: participant_data["championId"]
		})

import struct

def team_ids_to_bytes(summoner_ids: list):
	summoner_ids.sort()
	return struct.pack('QQQQQ', *summoner_ids)

def team_bytes_to_ids(data: bytes):
	return list(struct.unpack('QQQQQ', data))
