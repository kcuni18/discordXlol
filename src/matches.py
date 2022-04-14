from array import array
import database as db
import summoners
import util

with open('src/queries/insert_match.sql') as file:
	insert_match_query = file.read()
with open('src/queries/insert_participant.sql') as file:
	insert_participant_query = file.read()

def get_by_id(id: int):
	data = db.select(f'SELECT * FROM match WHERE id=:id', {'id':id})
	if len(data) != 1:
		raise KeyError(f'Match {id} is not recorded.')
	return data

def is_recorded(id: int):
	try:
		get_by_id(id)
		return True
	except KeyError:
		return False

def record(json_data: dict):
	db.execute(insert_match_query, {
		'id' 		: json_data["info"]["gameId"],
		'duration' 	: json_data["info"]["gameDuration"],
		'name' 		: json_data["info"]["gameName"],
		'team_blue'	: util.generate_team_id(json_data["metadata"]["participants"][0:5]),
		'team_red' 	: util.generate_team_id(json_data["metadata"]["participants"][5:10]),
		'blue_win' 	: 1 if json_data["info"]["participants"][0]["win"] else 0
	})

	for i in range(0, 10):
		id = summoners.get_by_puuid(json_data["metadata"]["participants"][i])['id']
		participant_data = json_data["info"]["participants"][i]
		db.execute(insert_participant_query, {
			'summoner_id' 			: id,
			'match_id' 				: json_data["info"]["gameId"],
			'team' 					: 0 if i < 5 else 1,
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
