import requests
import json
from datetime import datetime, timezone


def parse_game_datetime(datetime_str):
        if "+" in datetime_str:
             datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z') 
        else:
             datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S').astimezone(timezone.utc),


def parse_live_game_data(raw_live_game_data):
    parsed_live_game_data = {
        "live_game_id": raw_live_game_data["idEvent"],
        "live_game_home_team_id": raw_live_game_data["idHomeTeam"],
        "live_game_away_team_id": raw_live_game_data["idAwayTeam"],
        "live_game_home_team_score": raw_live_game_data["intHomeScore"],
        "live_game_away_team_score": raw_live_game_data["intAwayScore"],
        "live_game_status": raw_live_game_data["strStatus"],
        "live_game_progress": raw_live_game_data["strProgress"],
        }
    return parsed_live_game_data

leagues = {
           "MLB": {"league_id": "4424", "season": "2023"}, 
           "NFL": {"league_id": "4391", "season": "2023"},
           "NBA": {"league_id": "4387", "season": "2023-2024"},
           "NHL": {"league_id": "4380", "season" : "2023-2024"},
           }

sample_league_live_games = {}

for league, league_info in leagues.items():
        league_id = league_info["league_id"]
        print(league, league_id)
        league_live_games_url = f"https://www.thesportsdb.com/api/v2/json/40130162/livescore.php?l={league_id}"
        league_live_games_data = requests.get(league_live_games_url)
        league_live_games_dict = json.loads(league_live_games_data.text)
        if league_live_games_dict["events"]:
                league_live_team_example = league_live_games_dict["events"][0]
                sample_league_live_games[league] = league_live_team_example
                for k, v in league_live_team_example.items():
                        print(k,v)
                print('---------------')

if sample_league_live_games["NFL"].keys() == sample_league_live_games["NBA"].keys() == sample_league_live_games["NHL"].keys():
        for league in leagues:
                print(league)
                if league in sample_league_live_games:
                        parsed_player_data = parse_live_game_data(sample_league_live_games[league])
                        for key, val in parsed_player_data.items():
                                print(key, val, type(val))
                        print("-----------------------")
else:
        print('Keys are different')