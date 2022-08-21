import json

with open("config.json", 'r') as file:
	data = json.loads(file.read())

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

data['lol']['match_id_prefix'] = _regions[data['lol']['region']]
