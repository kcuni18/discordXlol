CREATE TABLE IF NOT EXISTS champion(
	id 					INTEGER 	PRIMARY KEY,
	name				TEXT		NOT NULL
);
CREATE TABLE IF NOT EXISTS summoner_spell(
	id 					INTEGER 	PRIMARY KEY,
	name				TEXT		NOT NULL
);
CREATE TABLE IF NOT EXISTS item(
	id 					INTEGER 	PRIMARY KEY,
	name 				TEXT 		NOT NULL
);
CREATE TABLE IF NOT EXISTS perk(
	id 					INTEGER 	PRIMARY KEY,
	key 				TEXT 		NOT NULL,
	icon 				TEXT 		NOT NULL,
	name 				TEXT 		NOT NULL,
	shortDesc 			TEXT 		NOT NULL,
	longDesc 			TEXT 		NOT NULL
);
CREATE TABLE IF NOT EXISTS summoner(
	_id 				INTEGER 	PRIMARY KEY AUTOINCREMENT,
	discord_id 			INTEGER 	UNIQUE,

	accountId 			TEXT		NOT NULL,
	profileIconId		INTEGER		NOT NULL,
	revisionDate		INTEGER		NOT NULL,
	name				TEXT		NOT NULL,
	id					TEXT		NOT NULL,
	puuid				TEXT		NOT NULL,
	summonerLevel		INTEGER		NOT NULL
);
CREATE TABLE IF NOT EXISTS lobby(
	_id 				INTEGER 	PRIMARY KEY AUTOINCREMENT,
	tournamentCode 		TEXT 		NOT NULL UNIQUE,
	name 				TEXT 		,
	open 				INTEGER 	NOT NULL,

	summoner_id_0 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_1 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_2 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_3 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_4 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_5 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_6 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_7 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_8 		INTEGER 	REFERENCES summoner(_id),
	summoner_id_9 		INTEGER 	REFERENCES summoner(_id)
);
CREATE TABLE IF NOT EXISTS team(
	_id 				INTEGER 	PRIMARY KEY AUTOINCREMENT,
	summoner_id_0 		INTEGER 	NOT NULL 	REFERENCES summoner(_id),
	summoner_id_1 		INTEGER 	NOT NULL 	REFERENCES summoner(_id),
	summoner_id_2 		INTEGER 	NOT NULL 	REFERENCES summoner(_id),
	summoner_id_3 		INTEGER 	NOT NULL 	REFERENCES summoner(_id),
	summoner_id_4 		INTEGER 	NOT NULL 	REFERENCES summoner(_id),
	name 				TEXT 		UNIQUE
);
CREATE TABLE IF NOT EXISTS match(
	gameCreation			INTEGER 	NOT NULL,
	gameDuration			INTEGER 	NOT NULL,
	gameEndTimestamp		INTEGER 	NOT NULL,
	gameId					INTEGER 	PRIMARY KEY,
	gameMode				TEXT 		NOT NULL,
	gameName				TEXT 		NOT NULL,
	gameStartTimestamp		INTEGER 	NOT NULL,
	gameType				TEXT 		NOT NULL,
	gameVersion				TEXT 		NOT NULL,
	mapId					INTEGER 	NOT NULL,
	platformId				TEXT 		NOT NULL,
	queueId					INTEGER 	NOT NULL,
	tournamentCode			TEXT 		NOT NULL
);
CREATE TABLE IF NOT EXISTS participant_team(
	_id 				INTEGER 	PRIMARY KEY AUTOINCREMENT,
	match_id 			INTEGER 	NOT NULL 	REFERENCES match(gameId),
	team_id 			INTEGER 	NOT NULL 	REFERENCES team(id),
	side 				TEXT 		NOT NULL,

	ban_0 				INTEGER 	REFERENCES champion(id),
	ban_1 				INTEGER 	REFERENCES champion(id),
	ban_2 				INTEGER 	REFERENCES champion(id),
	ban_3 				INTEGER 	REFERENCES champion(id),
	ban_4 				INTEGER 	REFERENCES champion(id),

	baron_first 		INTEGER 	NOT NULL,
	baron_kills 		INTEGER 	NOT NULL,
	champion_first 		INTEGER 	NOT NULL,
	champion_kills 		INTEGER 	NOT NULL,
	dragon_first 		INTEGER 	NOT NULL,
	dragon_kills 		INTEGER 	NOT NULL,
	inhibitor_first 	INTEGER 	NOT NULL,
	inhibitor_kills 	INTEGER 	NOT NULL,
	rift_herald_first 	INTEGER 	NOT NULL,
	rift_herald_kills 	INTEGER 	NOT NULL,
	tower_first 		INTEGER 	NOT NULL,
	tower_kills 		INTEGER 	NOT NULL,
	win 				INTEGER 	NOT NULL
);
CREATE TABLE IF NOT EXISTS participant(
	_id 							INTEGER 		PRIMARY KEY AUTOINCREMENT,
	match_id 						INTEGER 		NOT NULL 	REFERENCES match(gameId),
	summoner_id 					INTEGER 		NOT NULL 	REFERENCES summoner(_id),
	participant_team 				INTEGER 		NOT NULL 	REFERENCES participant_team(_id),

	assists							INTEGER			NOT NULL,
	baronKills						INTEGER			NOT NULL,
	bountyLevel						INTEGER			NOT NULL,
	champExperience					INTEGER			NOT NULL,
	champLevel						INTEGER			NOT NULL,
	championId						INTEGER			NOT NULL,
	championName					TEXT			NOT NULL,
	championTransform				INTEGER			NOT NULL,
	consumablesPurchased			INTEGER			NOT NULL,
	damageDealtToBuildings			INTEGER			NOT NULL,
	damageDealtToObjectives			INTEGER			NOT NULL,
	damageDealtToTurrets			INTEGER			NOT NULL,
	damageSelfMitigated				INTEGER			NOT NULL,
	deaths							INTEGER			NOT NULL,
	detectorWardsPlaced				INTEGER			NOT NULL,
	doubleKills						INTEGER			NOT NULL,
	dragonKills						INTEGER			NOT NULL,
	firstBloodAssist				INTEGER			NOT NULL,
	firstBloodKill					INTEGER			NOT NULL,
	firstTowerAssist				INTEGER			NOT NULL,
	firstTowerKill					INTEGER			NOT NULL,
	gameEndedInEarlySurrender		INTEGER			NOT NULL,
	gameEndedInSurrender			INTEGER			NOT NULL,
	goldEarned						INTEGER			NOT NULL,
	goldSpent						INTEGER			NOT NULL,
	individualPosition				TEXT			NOT NULL,
	inhibitorKills					INTEGER			NOT NULL,
	inhibitorTakedowns				INTEGER			NOT NULL,
	inhibitorsLost					INTEGER			NOT NULL,
	item0							INTEGER			NOT NULL,
	item1							INTEGER			NOT NULL,
	item2							INTEGER			NOT NULL,
	item3							INTEGER			NOT NULL,
	item4							INTEGER			NOT NULL,
	item5							INTEGER			NOT NULL,
	item6							INTEGER			NOT NULL,
	itemsPurchased					INTEGER			NOT NULL,
	killingSprees					INTEGER			NOT NULL,
	kills							INTEGER			NOT NULL,
	lane							TEXT			NOT NULL,
	largestCriticalStrike			INTEGER			NOT NULL,
	largestKillingSpree				INTEGER			NOT NULL,
	largestMultiKill				INTEGER			NOT NULL,
	longestTimeSpentLiving			INTEGER			NOT NULL,
	magicDamageDealt				INTEGER			NOT NULL,
	magicDamageDealtToChampions		INTEGER			NOT NULL,
	magicDamageTaken				INTEGER			NOT NULL,
	neutralMinionsKilled			INTEGER			NOT NULL,
	nexusKills						INTEGER			NOT NULL,
	nexusTakedowns					INTEGER			NOT NULL,
	nexusLost						INTEGER			NOT NULL,
	objectivesStolen				INTEGER			NOT NULL,
	objectivesStolenAssists			INTEGER			NOT NULL,
	participantId					INTEGER			NOT NULL,
	pentaKills						INTEGER			NOT NULL,
	physicalDamageDealt				INTEGER			NOT NULL,
	physicalDamageDealtToChampions	INTEGER			NOT NULL,
	physicalDamageTaken				INTEGER			NOT NULL,
	profileIcon						INTEGER			NOT NULL,
	puuid							TEXT			NOT NULL,
	quadraKills						INTEGER			NOT NULL,
	riotIdName						TEXT			NOT NULL,
	riotIdTagline					TEXT			NOT NULL,
	role							TEXT			NOT NULL,
	sightWardsBoughtInGame			INTEGER			NOT NULL,
	spell1Casts						INTEGER			NOT NULL,
	spell2Casts						INTEGER			NOT NULL,
	spell3Casts						INTEGER			NOT NULL,
	spell4Casts						INTEGER			NOT NULL,
	summoner1Casts					INTEGER			NOT NULL,
	summoner1Id						INTEGER			NOT NULL,
	summoner2Casts					INTEGER			NOT NULL,
	summoner2Id						INTEGER			NOT NULL,
	summonerId						TEXT			NOT NULL,
	summonerLevel					INTEGER			NOT NULL,
	summonerName					TEXT			NOT NULL,
	teamEarlySurrendered			INTEGER			NOT NULL,
	teamId							INTEGER			NOT NULL,
	teamPosition					TEXT			NOT NULL,
	timeCCingOthers					INTEGER			NOT NULL,
	timePlayed						INTEGER			NOT NULL,
	totalDamageDealt				INTEGER			NOT NULL,
	totalDamageDealtToChampions		INTEGER			NOT NULL,
	totalDamageShieldedOnTeammates	INTEGER			NOT NULL,
	totalDamageTaken				INTEGER			NOT NULL,
	totalHeal						INTEGER			NOT NULL,
	totalHealsOnTeammates			INTEGER			NOT NULL,
	totalMinionsKilled				INTEGER			NOT NULL,
	totalTimeCCDealt				INTEGER			NOT NULL,
	totalTimeSpentDead				INTEGER			NOT NULL,
	totalUnitsHealed				INTEGER			NOT NULL,
	tripleKills						INTEGER			NOT NULL,
	trueDamageDealt					INTEGER			NOT NULL,
	trueDamageDealtToChampions		INTEGER			NOT NULL,
	trueDamageTaken					INTEGER			NOT NULL,
	turretKills						INTEGER			NOT NULL,
	turretTakedowns					INTEGER			NOT NULL,
	turretsLost						INTEGER			NOT NULL,
	unrealKills						INTEGER			NOT NULL,
	visionScore						INTEGER			NOT NULL,
	visionWardsBoughtInGame			INTEGER			NOT NULL,
	wardsKilled						INTEGER			NOT NULL,
	wardsPlaced						INTEGER			NOT NULL,
	win								INTEGER			NOT NULL,

	perk_defence					INTEGER			NOT NULL REFERENCES perk(id),
	perk_flex						INTEGER			NOT NULL REFERENCES perk(id),
	perk_offense					INTEGER			NOT NULL REFERENCES perk(id),
	perk_style_primary_0 			INTEGER 		NOT NULL REFERENCES perk(id),
	perk_style_primary_1 			INTEGER 		NOT NULL REFERENCES perk(id),
	perk_style_primary_2 			INTEGER 		NOT NULL REFERENCES perk(id),
	perk_style_primary_3 			INTEGER 		NOT NULL REFERENCES perk(id),
	perk_style_secondary_0 			INTEGER 		NOT NULL REFERENCES perk(id),
	perk_style_secondary_1 			INTEGER 		NOT NULL REFERENCES perk(id)
);