INSERT INTO participant(
	summoner_id,
	match_id,
	team,
	kills,
	assists,
	deaths,
	double_kills,
	triple_kills,
	quadra_kills,
	penta_kills,
	total_minion_kills,
	gold_earned,
	gold_spent,
	total_damage_dealt,
	total_damage_dealt_to_champions,
	total_damage_shielded_on_teammates,
	total_damage_taken,
	physical_damage_dealt,
	physical_damage_dealt_to_champions,
	physical_damage_taken,
	magic_damage_dealt,
	magic_damage_dealt_to_champions,
	magic_damage_taken,
	true_damage_dealt,
	true_damage_dealt_to_champions,
	true_damage_taken,
	total_heal,
	total_heal_on_teammates,
	self_mitigated_damage,
	damage_dealt_to_turrets,
	damage_dealt_to_objectives,
	damage_dealt_to_buildings,
	time_ccing_others,
	spell_1_casts,
	spell_2_casts,
	spell_3_casts,
	spell_4_casts,
	summoner_1_casts,
	summoner_1_id,
	summoner_2_casts,
	summoner_2_id,
	baron_kills,
	turret_kills,
	turret_takedowns,
	turrets_lost,
	bounty_level,
	vision_score,
	vision_wards_bought,
	wards_killed,
	wards_placed,
	champ_experience,
	champ_level,
	champ_id
)
VALUES(
	:summoner_id,
	:match_id,
	:team,
	:kills,
	:assists,
	:deaths,
	:double_kills,
	:triple_kills,
	:quadra_kills,
	:penta_kills,
	:total_minion_kills,
	:gold_earned,
	:gold_spent,
	:total_damage_dealt,
	:total_damage_dealt_to_champions,
	:total_damage_shielded_on_teammates,
	:total_damage_taken,
	:physical_damage_dealt,
	:physical_damage_dealt_to_champions,
	:physical_damage_taken,
	:magic_damage_dealt,
	:magic_damage_dealt_to_champions,
	:magic_damage_taken,
	:true_damage_dealt,
	:true_damage_dealt_to_champions,
	:true_damage_taken,
	:total_heal,
	:total_heal_on_teammates,
	:self_mitigated_damage,
	:damage_dealt_to_turrets,
	:damage_dealt_to_objectives,
	:damage_dealt_to_buildings,
	:time_ccing_others,
	:spell_1_casts,
	:spell_2_casts,
	:spell_3_casts,
	:spell_4_casts,
	:summoner_1_casts,
	:summoner_1_id,
	:summoner_2_casts,
	:summoner_2_id,
	:baron_kills,
	:turret_kills,
	:turret_takedowns,
	:turrets_lost,
	:bounty_level,
	:vision_score,
	:vision_wards_bought,
	:wards_killed,
	:wards_placed,
	:champ_experience,
	:champ_level,
	:champ_id
);