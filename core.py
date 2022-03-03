import league_api as lol
import summoners
from table_file import *
from util import *

# global variables
matches_file = None


def init():
    # matches file
    attrib = FileAttributes()
    attrib.insert("match_puuid", ATTRIBUTE_TYPE_STRING, 15)
    attrib.insert("team_1", ATTRIBUTE_TYPE_STRING, 78 * 5)
    attrib.insert("team_2", ATTRIBUTE_TYPE_STRING, 78 * 5)
    attrib.insert("win", ATTRIBUTE_TYPE_INT, 1)

    global matches_file
    matches_file = TableFile('matches.bin', attrib)

    # summoners
    summoners.init()


def terminate():
    summoners.write()


def winrate_by_discord(discord_id):
    wins = 0
    losses = 0
    puuid = summoners.get_puuid_by_discord_name(discord_id)
    if puuid is None:
        return "Discord account is not linked!"
    for i in range(matches_file.count):
        # print("Getting ", i , " game")
        row = matches_file.row_get(i)
        teammates = split_team_puuids(row["team_1"])
        if puuid in teammates:
            # print("Found on team 1")
            wins += row["win"]
            losses += 0 if row["win"] == 1 else 1
        teammates = split_team_puuids(row["team_2"])
        if puuid in teammates:
            # print("Found on team 2")
            wins += 1 if row["win"] == 0 else 0
            losses += row["win"]
    # return wins, losses
    winrate = wins / (wins + losses) * 100
    return "{} has a winrate of {:.2f}% with {} wins and {} losses".format(summoners.get_name_by_puuid(puuid), winrate, wins, losses)


def winrate_by_name(name):
    wins = 0
    losses = 0
    puuid = summoners.get_puuid_by_name(name)
    if puuid is None:
        return "{} does not exist".format(name)
    for i in range(matches_file.count):
        # print("Getting ", i , " game")
        row = matches_file.row_get(i)
        teammates = split_team_puuids(row["team_1"])
        if puuid in teammates:
            # print("Found on team 1")
            wins += row["win"]
            losses += 0 if row["win"] == 1 else 1
        teammates = split_team_puuids(row["team_2"])
        if puuid in teammates:
            # print("Found on team 2")
            wins += 1 if row["win"] == 0 else 0
            losses += row["win"]
    # return wins, losses
    winrate = wins / (wins + losses) * 100
    return "{} has a winrate of {:.2f}% with {} wins and {} losses".format(name, winrate, wins, losses)


def winrate_by_team(players):
    players_puuid = []
    for player in players:
        temp = summoners.get_puuid_by_discord_name(player)
        if temp is None:
            return [player, " is not linked"]
        players_puuid.append(temp)
    team = generate_team_id(players_puuid)
    wins = 0
    losses = 0
    for i in range(matches_file.count):
        row = matches_file.row_get(i)
        if row["team_1"] == team:
            wins += row["win"]
            losses += 0 if row["win"] == 1 else 1
        elif row["team_2"] == team:
            wins += 1 if row["win"] == 0 else 0
            losses += row["win"]
    if wins == 0 and losses == 0:
        return "Team has not played any games together"
    return "Team {}\nWinrate: {:.2f}% \nWins: {} \nLosses: {}".format(get_team_names(team), wins/(wins+losses)*100, wins, losses)


def winrate_for_best_teams(team_count=1, min_games=1):
    result = ""
    teams = {}
    for i in range(matches_file.count):
        row = matches_file.row_get(i)
        try:
            teams[row["team_1"]][0] += row["win"]
            teams[row["team_1"]][1] += 0 if row["win"] == 1 else 1
        except:
            teams[row["team_1"]] = [row["win"], 0 if row["win"] == 1 else 1]
        try:
            teams[row["team_2"]][0] += 1 if row["win"] == 0 else 0
            teams[row["team_2"]][1] += row["win"]
        except:
            teams[row["team_2"]] = [1 if row["win"] == 0 else 0, row["win"]]
    sorted_teams = []
    for team in teams:
        if teams[team][0] + teams[team][1] >= min_games:
            sorted_teams.append({
                'team': get_team_names(team),
                'winrate': teams[team][0] / (teams[team][0] + teams[team][1]) * 100,
                'wins': teams[team][0],
                'losses': teams[team][1]
            })
    sorted_teams.sort(key=lambda x: x['winrate'], reverse=True)
    for i in range(min(team_count, len(sorted_teams))):
        result += "Team {}\nWinrate: {:.2f}% \nWins: {} \nLosses: {}\n `--------------------------------------------------------------------------------------------`\n" \
            .format(sorted_teams[i]['team'],
                    sorted_teams[i]['winrate'],
                    sorted_teams[i]['wins'],
                    sorted_teams[i]['losses'])
    if result == "":
        return "No teams meet the criteria"
    return result


def record_games(name, count=1):
    not_counted = 0
    puuid = summoners.get_puuid_by_name(name.lower())
    match_ids = lol.get_match_ids(puuid, 100)
    for match_id in match_ids:
        match_info = lol.get_match_info(match_id)
        if match_info["info"]["gameType"] != "CUSTOM_GAME":
            print("Match type is {}. Skipping.".format(match_info["info"]["gameType"]))
        elif len(match_info["metadata"]["participants"]) != 10:
            print("Nr of participants is {}. Skipping.".format(len(match_info["metadata"]["participants"])))
        else:
            match_found = False
            for i in range(matches_file.count):
                row = matches_file.attrib_get(i, "match_puuid")
                if row == match_info["metadata"]["matchId"]:
                    print("Match already recorded. Skipping.")
                    match_found = True
            if not match_found:
                not_counted += 1
                print("Adding match with id {}.".format(match_info['metadata']['matchId']))
                for participant in match_info['metadata']['participants']:
                    if summoners.get_name_by_puuid(participant) is None:
                        summoners.add_by_puuid(participant)
                        print("Found new summoner '{}'.".format(summoners.get_name_by_puuid(participant)))
                matches_file.row_append({
                    'match_puuid': match_info['metadata']['matchId'],
                    'team_1': ''.join(sorted(match_info['metadata']['participants'][0:5])),
                    'team_2': ''.join(sorted(match_info['metadata']['participants'][5:10])),
                    'win': 1 if match_info['info']['participants'][0]['win'] else 0
                })
            count = count - 1
            if count == 0:
                break
        return "Out of {} games, {} were new and recorded".format(count, not_counted)


def unlink_account(discord_id):
    if summoners.unlink_discord(discord_id):
        summoners.write()
        return "Account unlinked successfully."
    else:
        return "Account is not linked."


def link_account(discord_id, summoner):
    if summoners.link_discord(discord_id, summoner):
        summoners.write()
        return "Account linked successfully"
    else:
        return "Already linked or account name does not match"


def find_account(discord_id):
    if summoners.get_name_by_puuid(summoners.get_puuid_by_discord_name(discord_id)) is None:
        return "Account is not linked"
    else:
        return summoners.get_name_by_puuid(summoners.get_puuid_by_discord_name(discord_id)) + " is the linked account."

###### TESTING ######

# load files
init()

"""
for player in summoners.data:
    if "discord_name" not in player:
        player["discord_name"] = 0
        print("Dsicord key missing on :", player["name"])
"""

# code to add all summoners present in the matches file
# for i in range(matches_file.count):
#	row = matches_file.row_get(i)
#	team_1 = split_team_puuids(row["team_1"])
#	team_2 = split_team_puuids(row["team_2"])
#	for puuid in team_1 + team_2:
#		if summoners.get_name_by_puuid(puuid) == None:
#			summoners.add_by_puuid(puuid)
#			print("Found new summoner '{}'.".format(summoners.get_name_by_puuid(puuid)))


# winrate_for_best_teams(team_count=2,min_games=2)


# print(winrate_by_name("its jungle gap"))


# write and close files
terminate()