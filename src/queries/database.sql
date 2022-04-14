CREATE TABLE IF NOT EXISTS champion(
	id 					INTEGER 	PRIMARY KEY,
	name				TEXT		NOT NULL
);
CREATE TABLE IF NOT EXISTS summoner_spell(
	id 					INTEGER 	PRIMARY KEY,
	name				TEXT		NOT NULL
);
CREATE TABLE IF NOT EXISTS summoner(
	id 					INTEGER 	PRIMARY KEY,
	puuid				TEXT		NOT NULL UNIQUE,
	name 				TEXT 		NOT NULL UNIQUE,
	profile_icon_id		INTEGER		NOT NULL,
	level				INTEGER		NOT NULL,
	discord_id 			INTEGER		UNIQUE
);
CREATE TABLE IF NOT EXISTS match(
	id 					INTEGER 	PRIMARY KEY,
	duration 			INTEGER 	NOT NULL,
	name 				TEXT 		NOT NULL,

	team_blue			TEXT		NOT NULL,
	team_red			TEXT		NOT NULL,
	blue_win			INTEGER		NOT NULL
);
CREATE TABLE IF NOT EXISTS participant(
	id 					INTEGER 	PRIMARY KEY 	AUTOINCREMENT,
	summoner_id			INTEGER 	NOT NULL 		REFERENCES summoner(id),
	match_id 			INTEGER 	NOT NULL 		REFERENCES match(id),
	team				INTEGER		NOT NULL,

	kills				INTEGER		NOT NULL,
	assists 			INTEGER		NOT NULL,
	deaths				INTEGER		NOT NULL,

	double_kills		INTEGER 	NOT NULL,
	triple_kills		INTEGER 	NOT NULL,
	quadra_kills		INTEGER 	NOT NULL,
	penta_kills			INTEGER 	NOT NULL,

	total_minion_kills	INTEGER		NOT NULL,

	gold_earned			INTEGER		NOT NULL,
	gold_spent			INTEGER		NOT NULL,

	total_damage_dealt					INTEGER		NOT NULL,
	total_damage_dealt_to_champions		INTEGER		NOT NULL,
	total_damage_shielded_on_teammates	INTEGER		NOT NULL,
	total_damage_taken					INTEGER		NOT NULL,
	physical_damage_dealt				INTEGER		NOT NULL,
	physical_damage_dealt_to_champions	INTEGER		NOT NULL,
	physical_damage_taken				INTEGER		NOT NULL,
	magic_damage_dealt					INTEGER		NOT NULL,
	magic_damage_dealt_to_champions		INTEGER		NOT NULL,
	magic_damage_taken					INTEGER		NOT NULL,
	true_damage_dealt					INTEGER		NOT NULL,
	true_damage_dealt_to_champions		INTEGER		NOT NULL,
	true_damage_taken					INTEGER		NOT NULL,
	total_heal							INTEGER		NOT NULL,
	total_heal_on_teammates				INTEGER		NOT NULL,
	self_mitigated_damage				INTEGER		NOT NULL,
	damage_dealt_to_turrets				INTEGER 	NOT NULL,
	damage_dealt_to_objectives			INTEGER 	NOT NULL,
	damage_dealt_to_buildings			INTEGER 	NOT NULL,
	time_ccing_others					INTEGER		NOT NULL,

	spell_1_casts		INTEGER		NOT NULL,
	spell_2_casts		INTEGER		NOT NULL,
	spell_3_casts		INTEGER		NOT NULL,
	spell_4_casts		INTEGER		NOT NULL,
	summoner_1_casts	INTEGER		NOT NULL,
	summoner_1_id		INTEGER		NOT NULL REFERENCES summoner_spell(id),
	summoner_2_casts	INTEGER		NOT NULL,
	summoner_2_id		INTEGER		NOT NULL REFERENCES summoner_spell(id),

	baron_kills			INTEGER		NOT NULL,
	turret_kills		INTEGER		NOT NULL,
	turret_takedowns	INTEGER		NOT NULL,
	turrets_lost		INTEGER		NOT NULL,
	bounty_level		INTEGER		NOT NULL,

	vision_score		INTEGER		NOT NULL,
	vision_wards_bought	INTEGER		NOT NULL,
	wards_killed		INTEGER		NOT NULL,
	wards_placed		INTEGER		NOT NULL,

	champ_experience	INTEGER		NOT NULL,
	champ_level			INTEGER		NOT NULL,
	champ_id			INTEGER		NOT NULL REFERENCES champion(id)
);

/* champions */
INSERT INTO champion(id, name) VALUES
(266, "Aatrox"),
(103, "Ahri"),
(84, "Akali"),
(166, "Akshan"),
(12, "Alistar"),
(32, "Amumu"),
(34, "Anivia"),
(1, "Annie"),
(523, "Aphelios"),
(22, "Ashe"),
(136, "Aurelion Sol"),
(268, "Azir"),
(432, "Bard"),
(53, "Blitzcrank"),
(63, "Brand"),
(201, "Braum"),
(51, "Caitlyn"),
(164, "Camille"),
(69, "Cassiopeia"),
(31, "Cho'Gath"),
(42, "Corki"),
(122, "Darius"),
(131, "Diana"),
(119, "Draven"),
(36, "Dr. Mundo"),
(245, "Ekko"),
(60, "Elise"),
(28, "Evelynn"),
(81, "Ezreal"),
(9, "Fiddlesticks"),
(114, "Fiora"),
(105, "Fizz"),
(3, "Galio"),
(41, "Gangplank"),
(86, "Garen"),
(150, "Gnar"),
(79, "Gragas"),
(104, "Graves"),
(887, "Gwen"),
(120, "Hecarim"),
(74, "Heimerdinger"),
(420, "Illaoi"),
(39, "Irelia"),
(427, "Ivern"),
(40, "Janna"),
(59, "Jarvan IV"),
(24, "Jax"),
(126, "Jayce"),
(202, "Jhin"),
(222, "Jinx"),
(145, "Kai'Sa"),
(429, "Kalista"),
(43, "Karma"),
(30, "Karthus"),
(38, "Kassadin"),
(55, "Katarina"),
(10, "Kayle"),
(141, "Kayn"),
(85, "Kennen"),
(121, "Kha'Zix"),
(203, "Kindred"),
(240, "Kled"),
(96, "Kog'Maw"),
(7, "LeBlanc"),
(64, "Lee Sin"),
(89, "Leona"),
(876, "Lillia"),
(127, "Lissandra"),
(236, "Lucian"),
(117, "Lulu"),
(99, "Lux"),
(54, "Malphite"),
(90, "Malzahar"),
(57, "Maokai"),
(11, "Master Yi"),
(21, "Miss Fortune"),
(62, "Wukong"),
(82, "Mordekaiser"),
(25, "Morgana"),
(267, "Nami"),
(75, "Nasus"),
(111, "Nautilus"),
(518, "Neeko"),
(76, "Nidalee"),
(56, "Nocturne"),
(20, "Nunu & Willump"),
(2, "Olaf"),
(61, "Orianna"),
(516, "Ornn"),
(80, "Pantheon"),
(78, "Poppy"),
(555, "Pyke"),
(246, "Qiyana"),
(133, "Quinn"),
(497, "Rakan"),
(33, "Rammus"),
(421, "Rek'Sai"),
(526, "Rell"),
(888, "Renata Glasc"),
(58, "Renekton"),
(107, "Rengar"),
(92, "Riven"),
(68, "Rumble"),
(13, "Ryze"),
(360, "Samira"),
(113, "Sejuani"),
(235, "Senna"),
(147, "Seraphine"),
(875, "Sett"),
(35, "Shaco"),
(98, "Shen"),
(102, "Shyvana"),
(27, "Singed"),
(14, "Sion"),
(15, "Sivir"),
(72, "Skarner"),
(37, "Sona"),
(16, "Soraka"),
(50, "Swain"),
(517, "Sylas"),
(134, "Syndra"),
(223, "Tahm Kench"),
(163, "Taliyah"),
(91, "Talon"),
(44, "Taric"),
(17, "Teemo"),
(412, "Thresh"),
(18, "Tristana"),
(48, "Trundle"),
(23, "Tryndamere"),
(4, "Twisted Fate"),
(29, "Twitch"),
(77, "Udyr"),
(6, "Urgot"),
(110, "Varus"),
(67, "Vayne"),
(45, "Veigar"),
(161, "Vel'Koz"),
(711, "Vex"),
(254, "Vi"),
(234, "Viego"),
(112, "Viktor"),
(8, "Vladimir"),
(106, "Volibear"),
(19, "Warwick"),
(498, "Xayah"),
(101, "Xerath"),
(5, "Xin Zhao"),
(157, "Yasuo"),
(777, "Yone"),
(83, "Yorick"),
(350, "Yuumi"),
(154, "Zac"),
(238, "Zed"),
(221, "Zeri"),
(115, "Ziggs"),
(26, "Zilean"),
(142, "Zoe"),
(143, "Zyra");

/* summoner_spells */
INSERT INTO summoner_spell(id, name) VALUES
(21, "Barrier"),
(1, "Cleanse"),
(14, "Ignite"),
(3, "Exhaust"),
(4, "Flash"),
(6, "Ghost"),
(7, "Heal"),
(13, "Clarity"),
(30, "To the King!"),
(31, "Poro Toss"),
(11, "Smite"),
(39, "Mark"),
(32, "Mark"),
(12, "Teleport"),
(54, "Placeholder"),
(55, "Placeholder and Attack-Smite");
