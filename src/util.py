import summoners


# split team puuid into array of summoner puuid
def split_team_puuids(team):
    return [team[index: index + 78] for index in range(0, len(team), 78)]


# get array of summoner names from team puuid
def get_team_names(team):
    return [summoners.get_name_by_puuid(puuid) for puuid in split_team_puuids(team)]


# sort array of summoner puuid to form a unique team puuid
def generate_team_id(player_puuids):
    return "".join(sorted(player_puuids))
