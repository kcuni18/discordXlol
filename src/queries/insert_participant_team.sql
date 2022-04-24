INSERT INTO participant_team(
	match_id,
	team_id,
	side,

	ban_0,
	ban_1,
	ban_2,
	ban_3,
	ban_4,

	baron_first,
	baron_kills,
	champion_first,
	champion_kills,
	dragon_first,
	dragon_kills,
	inhibitor_first,
	inhibitor_kills,
	rift_herald_first,
	rift_herald_kills,
	tower_first,
	tower_kills,
	win
)
VALUES (
	:match_id,
	:team_id,
	:side,

	:ban_0,
	:ban_1,
	:ban_2,
	:ban_3,
	:ban_4,

	:baron_first,
	:baron_kills,
	:champion_first,
	:champion_kills,
	:dragon_first,
	:dragon_kills,
	:inhibitor_first,
	:inhibitor_kills,
	:rift_herald_first,
	:rift_herald_kills,
	:tower_first,
	:tower_kills,
	:win
)