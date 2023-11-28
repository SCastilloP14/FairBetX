import requests
import json
from datetime import datetime



def parse_team_data(raw_team_data):
    parsed_team_data = {
        "team_id": raw_team_data["idTeam"],
        "team_name": raw_team_data["strTeam"],
        "team_short_name": raw_team_data["strTeamShort"],
        "team_formed_year": raw_team_data["intFormedYear"],
        "team_sport": raw_team_data["strSport"],
        "team_leauge_1_id": raw_team_data["idLeague"],
        "team_leauge_2_id": raw_team_data["idLeague2"],
        "team_leauge_3_id": raw_team_data["idLeague3"],
        "team_leauge_4_id": raw_team_data["idLeague4"],
        "team_leauge_5_id": raw_team_data["idLeague5"],
        "team_leauge_6_id": raw_team_data["idLeague6"],
        "team_leauge_7_id": raw_team_data["idLeague7"],
        "team_stadium": raw_team_data["strStadium"],
        "team_stadium_description": raw_team_data["strStadiumDescription"],
        "team_stadium_capacity": raw_team_data["intStadiumCapacity"] if raw_team_data["intStadiumCapacity"]!=0 else None,
        "team_location": raw_team_data["strStadiumLocation"],
        "team_country": raw_team_data["strCountry"],
        "team_gender": raw_team_data["strGender"],
        "team_description": raw_team_data["strDescriptionEN"],
        "team_badge": raw_team_data["strTeamBadge"],
        "team_jersey": raw_team_data["strTeamJersey"],
        "team_logo": raw_team_data["strTeamLogo"]
        }
    return parsed_team_data


leagues = {
           "MLB": {"league_id": "4424", "season": "2023"}, 
           "NFL": {"league_id": "4391", "season": "2023"},
           "NBA": {"league_id": "4387", "season": "2023-2024"},
           "NHL": {"league_id": "4380", "season" : "2023-2024"},
           }
sample_league_teams = {}

for league in leagues:
        league_teams_url = f"https://www.thesportsdb.com/api/v1/json/3/search_all_teams.php?l={league}"
        league_teams_data = requests.get(league_teams_url)
        league_teams_dict = json.loads(league_teams_data.text)
        league_team_example = league_teams_dict["teams"][0]
        sample_league_teams[league] = league_team_example
        # for k, v in league_team_example.items():
        #     print(k,v)
        # print('---------------')

if sample_league_teams["NBA"].keys() == sample_league_teams["MLB"].keys() == sample_league_teams["NFL"].keys() == sample_league_teams["NHL"].keys():
        for league in leagues:
                print(league)
                parsed_team_data = parse_team_data(sample_league_teams[league])
                for key, val in parsed_team_data.items():
                        print(key, val, type(val))
                        if "team_leauge" in key:
                               print(f"key:{key}")
                               if val:
                                      print(f"val:{val}")
                print("-----------------------")
else:
        print('Keys are different')