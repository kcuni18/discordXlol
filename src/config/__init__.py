import json

with open("config.json", 'r') as file:
	data = json.loads(file.read())

credentials = data['credentials']
settings = data['settings']

_regions = {
	"BR"	: "BR1",
 	"EUNE"	: "EUN1",
 	"EUW"	: "EUW1",
 	"JP"	: "JP1",
 	"LAN"	: "LA1",
 	"LAS"	: "LA2",
 	"NA"	: "NA1",
 	"OCE"	: "OC1",
 	"RU"	: "RU",
	"TR"	: "TR1"
}

settings['lol']['match_id_prefix'] = _regions[settings['lol']['game_region']]
