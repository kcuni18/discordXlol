INSERT INTO participant(
	match_id,
	summoner_id,
	participant_team,
	ASSISTS,
	BARON_KILLS,
	BARRACKS_KILLED,
	BARRACKS_TAKEDOWNS,
	BOUNTY_LEVEL,
	CHAMPION_MISSION_STAT_0,
	CHAMPION_MISSION_STAT_1,
	CHAMPION_MISSION_STAT_2,
	CHAMPION_MISSION_STAT_3,
	CHAMPION_TRANSFORM,
	CHAMPIONS_KILLED,
	CONSUMABLES_PURCHASED,
	DOUBLE_KILLS,
	DRAGON_KILLS,
	EXP,
	FRIENDLY_DAMPEN_LOST,
	FRIENDLY_HQ_LOST,
	FRIENDLY_TURRET_LOST,
	GAME_ENDED_IN_EARLY_SURRENDER,
	GAME_ENDED_IN_SURRENDER,
	GOLD_EARNED,
	GOLD_SPENT,
	HQ_KILLED,
	HQ_TAKEDOWNS,
	ID,
	INDIVIDUAL_POSITION,
	ITEM0,
	ITEM1,
	ITEM2,
	ITEM3,
	ITEM4,
	ITEM5,
	ITEM6,
	ITEMS_PURCHASED,
	KEYSTONE_ID,
	KILLING_SPREES,
	LARGEST_CRITICAL_STRIKE,
	LARGEST_KILLING_SPREE,
	LARGEST_MULTI_KILL,
	LEVEL,
	LONGEST_TIME_SPENT_LIVING,
	MAGIC_DAMAGE_DEALT_PLAYER,
	MAGIC_DAMAGE_DEALT_TO_CHAMPIONS,
	MAGIC_DAMAGE_TAKEN,
	MINIONS_KILLED,
	MUTED_ALL,
	NAME,
	NEUTRAL_MINIONS_KILLED,
	NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE,
	NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE,
	NODE_CAPTURE,
	NODE_CAPTURE_ASSIST,
	NODE_NEUTRALIZE,
	NODE_NEUTRALIZE_ASSIST,
	NUM_DEATHS,
	OBJECTIVES_STOLEN,
	OBJECTIVES_STOLEN_ASSISTS,
	PENTA_KILLS,
	PERK0,
	PERK0_VAR1,
	PERK0_VAR2,
	PERK0_VAR3,
	PERK1,
	PERK1_VAR1,
	PERK1_VAR2,
	PERK1_VAR3,
	PERK2,
	PERK2_VAR1,
	PERK2_VAR2,
	PERK2_VAR3,
	PERK3,
	PERK3_VAR1,
	PERK3_VAR2,
	PERK3_VAR3,
	PERK4,
	PERK4_VAR1,
	PERK4_VAR2,
	PERK4_VAR3,
	PERK5,
	PERK5_VAR1,
	PERK5_VAR2,
	PERK5_VAR3,
	PERK_PRIMARY_STYLE,
	PERK_SUB_STYLE,
	STAT_PERK_0,
	STAT_PERK_1,
	STAT_PERK_2,
	PHYSICAL_DAMAGE_DEALT_PLAYER,
	PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS,
	PHYSICAL_DAMAGE_TAKEN,
	PING,
	PLAYER_POSITION,
	PLAYER_ROLE,
	PLAYER_SCORE_0,
	PLAYER_SCORE_1,
	PLAYER_SCORE_10,
	PLAYER_SCORE_11,
	PLAYER_SCORE_2,
	PLAYER_SCORE_3,
	PLAYER_SCORE_4,
	PLAYER_SCORE_5,
	PLAYER_SCORE_6,
	PLAYER_SCORE_7,
	PLAYER_SCORE_8,
	PLAYER_SCORE_9,
	QUADRA_KILLS,
	SIGHT_WARDS_BOUGHT_IN_GAME,
	SKIN,
	SPELL1_CAST,
	SPELL2_CAST,
	SPELL3_CAST,
	SPELL4_CAST,
	SUMMON_SPELL1_CAST,
	SUMMON_SPELL2_CAST,
	TEAM,
	TEAM_EARLY_SURRENDERED,
	TEAM_OBJECTIVE,
	TEAM_POSITION,
	TIME_CCING_OTHERS,
	TIME_OF_FROM_LAST_DISCONNECT,
	TIME_PLAYED,
	TIME_SPENT_DISCONNECTED,
	TOTAL_DAMAGE_DEALT,
	TOTAL_DAMAGE_DEALT_TO_BUILDINGS,
	TOTAL_DAMAGE_DEALT_TO_CHAMPIONS,
	TOTAL_DAMAGE_DEALT_TO_OBJECTIVES,
	TOTAL_DAMAGE_DEALT_TO_TURRETS,
	TOTAL_DAMAGE_SELF_MITIGATED,
	TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES,
	TOTAL_DAMAGE_TAKEN,
	TOTAL_HEAL,
	TOTAL_HEAL_ON_TEAMMATES,
	TOTAL_TIME_CROWD_CONTROL_DEALT,
	TOTAL_TIME_SPENT_DEAD,
	TOTAL_UNITS_HEALED,
	TRIPLE_KILLS,
	TRUE_DAMAGE_DEALT_PLAYER,
	TRUE_DAMAGE_DEALT_TO_CHAMPIONS,
	TRUE_DAMAGE_TAKEN,
	TURRET_TAKEDOWNS,
	TURRETS_KILLED,
	UNREAL_KILLS,
	VICTORY_POINT_TOTAL,
	VISION_SCORE,
	VISION_WARDS_BOUGHT_IN_GAME,
	WARD_KILLED,
	WARD_PLACED,
	WARD_PLACED_DETECTOR,
	WAS_AFK,
	WAS_AFK_AFTER_FAILED_SURRENDER,
	WAS_EARLY_SURRENDER_ACCOMPLICE,
	WAS_SURRENDER_DUE_TO_AFK,
	WIN
)
VALUES(
	:match_id,
	:summoner_id,
	:participant_team,
	:ASSISTS,
	:BARON_KILLS,
	:BARRACKS_KILLED,
	:BARRACKS_TAKEDOWNS,
	:BOUNTY_LEVEL,
	:CHAMPION_MISSION_STAT_0,
	:CHAMPION_MISSION_STAT_1,
	:CHAMPION_MISSION_STAT_2,
	:CHAMPION_MISSION_STAT_3,
	:CHAMPION_TRANSFORM,
	:CHAMPIONS_KILLED,
	:CONSUMABLES_PURCHASED,
	:DOUBLE_KILLS,
	:DRAGON_KILLS,
	:EXP,
	:FRIENDLY_DAMPEN_LOST,
	:FRIENDLY_HQ_LOST,
	:FRIENDLY_TURRET_LOST,
	:GAME_ENDED_IN_EARLY_SURRENDER,
	:GAME_ENDED_IN_SURRENDER,
	:GOLD_EARNED,
	:GOLD_SPENT,
	:HQ_KILLED,
	:HQ_TAKEDOWNS,
	:ID,
	:INDIVIDUAL_POSITION,
	:ITEM0,
	:ITEM1,
	:ITEM2,
	:ITEM3,
	:ITEM4,
	:ITEM5,
	:ITEM6,
	:ITEMS_PURCHASED,
	:KEYSTONE_ID,
	:KILLING_SPREES,
	:LARGEST_CRITICAL_STRIKE,
	:LARGEST_KILLING_SPREE,
	:LARGEST_MULTI_KILL,
	:LEVEL,
	:LONGEST_TIME_SPENT_LIVING,
	:MAGIC_DAMAGE_DEALT_PLAYER,
	:MAGIC_DAMAGE_DEALT_TO_CHAMPIONS,
	:MAGIC_DAMAGE_TAKEN,
	:MINIONS_KILLED,
	:MUTED_ALL,
	:NAME,
	:NEUTRAL_MINIONS_KILLED,
	:NEUTRAL_MINIONS_KILLED_ENEMY_JUNGLE,
	:NEUTRAL_MINIONS_KILLED_YOUR_JUNGLE,
	:NODE_CAPTURE,
	:NODE_CAPTURE_ASSIST,
	:NODE_NEUTRALIZE,
	:NODE_NEUTRALIZE_ASSIST,
	:NUM_DEATHS,
	:OBJECTIVES_STOLEN,
	:OBJECTIVES_STOLEN_ASSISTS,
	:PENTA_KILLS,
	:PERK0,
	:PERK0_VAR1,
	:PERK0_VAR2,
	:PERK0_VAR3,
	:PERK1,
	:PERK1_VAR1,
	:PERK1_VAR2,
	:PERK1_VAR3,
	:PERK2,
	:PERK2_VAR1,
	:PERK2_VAR2,
	:PERK2_VAR3,
	:PERK3,
	:PERK3_VAR1,
	:PERK3_VAR2,
	:PERK3_VAR3,
	:PERK4,
	:PERK4_VAR1,
	:PERK4_VAR2,
	:PERK4_VAR3,
	:PERK5,
	:PERK5_VAR1,
	:PERK5_VAR2,
	:PERK5_VAR3,
	:PERK_PRIMARY_STYLE,
	:PERK_SUB_STYLE,
	:STAT_PERK_0,
	:STAT_PERK_1,
	:STAT_PERK_2,
	:PHYSICAL_DAMAGE_DEALT_PLAYER,
	:PHYSICAL_DAMAGE_DEALT_TO_CHAMPIONS,
	:PHYSICAL_DAMAGE_TAKEN,
	:PING,
	:PLAYER_POSITION,
	:PLAYER_ROLE,
	:PLAYER_SCORE_0,
	:PLAYER_SCORE_1,
	:PLAYER_SCORE_10,
	:PLAYER_SCORE_11,
	:PLAYER_SCORE_2,
	:PLAYER_SCORE_3,
	:PLAYER_SCORE_4,
	:PLAYER_SCORE_5,
	:PLAYER_SCORE_6,
	:PLAYER_SCORE_7,
	:PLAYER_SCORE_8,
	:PLAYER_SCORE_9,
	:QUADRA_KILLS,
	:SIGHT_WARDS_BOUGHT_IN_GAME,
	:SKIN,
	:SPELL1_CAST,
	:SPELL2_CAST,
	:SPELL3_CAST,
	:SPELL4_CAST,
	:SUMMON_SPELL1_CAST,
	:SUMMON_SPELL2_CAST,
	:TEAM,
	:TEAM_EARLY_SURRENDERED,
	:TEAM_OBJECTIVE,
	:TEAM_POSITION,
	:TIME_CCING_OTHERS,
	:TIME_OF_FROM_LAST_DISCONNECT,
	:TIME_PLAYED,
	:TIME_SPENT_DISCONNECTED,
	:TOTAL_DAMAGE_DEALT,
	:TOTAL_DAMAGE_DEALT_TO_BUILDINGS,
	:TOTAL_DAMAGE_DEALT_TO_CHAMPIONS,
	:TOTAL_DAMAGE_DEALT_TO_OBJECTIVES,
	:TOTAL_DAMAGE_DEALT_TO_TURRETS,
	:TOTAL_DAMAGE_SELF_MITIGATED,
	:TOTAL_DAMAGE_SHIELDED_ON_TEAMMATES,
	:TOTAL_DAMAGE_TAKEN,
	:TOTAL_HEAL,
	:TOTAL_HEAL_ON_TEAMMATES,
	:TOTAL_TIME_CROWD_CONTROL_DEALT,
	:TOTAL_TIME_SPENT_DEAD,
	:TOTAL_UNITS_HEALED,
	:TRIPLE_KILLS,
	:TRUE_DAMAGE_DEALT_PLAYER,
	:TRUE_DAMAGE_DEALT_TO_CHAMPIONS,
	:TRUE_DAMAGE_TAKEN,
	:TURRET_TAKEDOWNS,
	:TURRETS_KILLED,
	:UNREAL_KILLS,
	:VICTORY_POINT_TOTAL,
	:VISION_SCORE,
	:VISION_WARDS_BOUGHT_IN_GAME,
	:WARD_KILLED,
	:WARD_PLACED,
	:WARD_PLACED_DETECTOR,
	:WAS_AFK,
	:WAS_AFK_AFTER_FAILED_SURRENDER,
	:WAS_EARLY_SURRENDER_ACCOMPLICE,
	:WAS_SURRENDER_DUE_TO_AFK,
	:WIN
);