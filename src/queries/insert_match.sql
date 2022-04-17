INSERT INTO match(
	id,
	duration,
	start,
	name,
	team_blue,
	team_red,
	blue_win
)
VALUES(
	:id,
	:duration,
	:start,
	:name,
	:team_blue,
	:team_red,
	:blue_win
);