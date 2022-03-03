import league_api as lol
import json

file_name = "summoners.json"
data = None
summoner_to_data = None
puuid_to_data = None
discord_to_data = None


def init():
    try:
        read()
    except FileNotFoundError:
        global data
        data = []
        global summoner_to_data
        summoner_to_data = {}
        global puuid_to_data
        puuid_to_data = {}
        with open(file_name, 'w') as file:
            file.write(json.dumps(data))


def read():
    global data
    with open(file_name, 'r') as file:
        data = json.loads(file.read())
    global summoner_to_data
    summoner_to_data = {}
    global puuid_to_data
    puuid_to_data = {}
    global discord_to_data
    discord_to_data = {}
    for obj in data:
        summoner_to_data[obj["name"]] = obj
        puuid_to_data[obj["puuid"]] = obj
        if obj["discord_name"] == 0:
            continue
        discord_to_data[obj["discord_name"]] = obj


def write():
    with open(file_name, 'w') as file:
        file.write(json.dumps(data))


def get_name_by_puuid(puuid):
    try:
        return puuid_to_data[puuid]["name"]
    except KeyError:
        return None


def get_discord_name_by_puuid(puuid):
    try:
        return puuid_to_data[puuid]["discord_name"]
    except KeyError:
        return None


def get_puuid_by_discord_name(dname):
    try:
        return discord_to_data[dname]["puuid"]
    except KeyError:
        return None


def get_puuid_by_name(name):
    try:
        return summoner_to_data[name]["puuid"]
    except KeyError:
        return None


def get_discord_name_by_name(name):
    try:
        return summoner_to_data[name]["discord_name"]
    except KeyError:
        return None


def add_by_name(name):
    summoner_data = lol.get_summoner_info_by_name(name)
    puuid = summoner_data["puuid"]
    data.append(summoner_data)
    summoner_to_data[name] = summoner_data
    puuid_to_data[puuid] = summoner_data


def add_by_puuid(puuid):
    summoner_data = lol.get_summoner_info_by_puuid(puuid)
    name = summoner_data["name"]
    data.append(summoner_data)
    summoner_to_data[name] = summoner_data
    puuid_to_data[puuid] = summoner_data


def link_discord(discord_name, summoner_name):
    try:
        for obj in data:
            if discord_name in obj.values():
                return False
        for obj in data:
            if obj["name"] == summoner_name:
                summoner_to_data[summoner_name]["discord_name"] = discord_name
                puuid_to_data[obj["puuid"]]["discord_name"] = discord_name
                discord_to_data[discord_name] = obj
                obj["discord_name"] = discord_name
                return True
        return False
    except KeyError:
        return False


def unlink_discord(discord_name):
    print(data)
    for obj in data:
        if "discord_name" not in obj:
            continue
        if obj["discord_name"] == int(discord_name):
            summoner_to_data[obj["name"]]["discord_name"] = 0
            puuid_to_data[obj["puuid"]]["discord_name"] = 0
            obj["discord_name"] = 0
            discord_to_data.pop(discord_name)
            return True
    return False


