import requests
import json


def parse_league_data(raw_team_data):
    parsed_league_data = {
        "league_id": raw_team_data["idLeague"],
        "league_sport": raw_team_data["strSport"],
        "league_name": raw_team_data["strLeague"],
        "league_alternative_name": raw_team_data["strLeagueAlternate"],
        "league_current_season": raw_team_data["strCurrentSeason"],
        "league_formed_year": raw_team_data["intFormedYear"],
        "league_first_event": raw_team_data["dateFirstEvent"],
        "league_gender": raw_team_data["strGender"],
        "league_country": raw_team_data["strCountry"],
        "league_description": raw_team_data["strDescriptionEN"],
        "league_badge": raw_team_data["strBadge"],
        "league_logo": raw_team_data["strLogo"],
        "league_trophy": raw_team_data["strTrophy"]
    }
    return parsed_league_data

leagues = {
           "MLB": {"league_id": "4424", "season": "2023"}, 
           "NFL": {"league_id": "4391", "season": "2023"},
           "NBA": {"league_id": "4387", "season": "2023-2024"},
           "NHL": {"league_id": "4380", "season" : "2023-2024"},
           }

sample_league_details = {}

for league, league_info in leagues.items():
        league_id = league_info["league_id"]
        print(league, league_id)

        league_details_url = f"https://www.thesportsdb.com/api/v1/json/40130162/lookupleague.php?id={league_id}"
        league_details_data = requests.get(league_details_url)
        league_details_dict = json.loads(league_details_data.text)
        league_details_example = league_details_dict["leagues"][0]
        sample_league_details[league] = league_details_example
        for k, v in league_details_example.items():
            print(k,v)
        print('---------------')

if sample_league_details["NBA"].keys() == sample_league_details["MLB"].keys() == sample_league_details["NFL"].keys() == sample_league_details["NHL"].keys():
        for league in leagues:
                print(league)
                parsed_league_data = parse_league_data(sample_league_details[league])
                for key, val in parsed_league_data.items():
                        print(key, val, type(val))
        print("-----------------------")
else:
        print('Keys are different')