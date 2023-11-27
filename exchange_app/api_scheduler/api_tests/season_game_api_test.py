import requests
import json
from datetime import datetime, timezone


def parse_game_datetime(datetime_str):
        if "+" in datetime_str:
             datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z') 
        else:
             datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S').astimezone(timezone.utc),


def parse_season_game_data(raw_season_game_data):
    parsed_season_game_data = {
        "season_game_id": raw_season_game_data["idEvent"],
        "season_game_name": raw_season_game_data["strEvent"],
        "season_game_alternative_name": raw_season_game_data["strEventAlternate"],
        "season_game_filename": raw_season_game_data["strFilename"],
        "season_game_season": raw_season_game_data["strSeason"],
        "season_game_home_team_id": raw_season_game_data["idHomeTeam"],
        "season_game_away_team_id": raw_season_game_data["idAwayTeam"],
        "season_game_home_team_score": raw_season_game_data["intHomeScore"],
        "season_game_away_team_score": raw_season_game_data["intAwayScore"],
        "season_game_round": raw_season_game_data["intRound"],
        "season_game_spectators": raw_season_game_data["intSpectators"],
        "season_game_official": raw_season_game_data["strOfficial"],
        "season_game_start_datetime": parse_game_datetime(raw_season_game_data["strTimestamp"]),
        "season_game_results": raw_season_game_data["strResult"],
        "season_game_venue": raw_season_game_data["strVenue"],
        "season_game_country": raw_season_game_data["strCountry"],
        "season_game_city": raw_season_game_data["strCity"],
        "season_game_status": raw_season_game_data["strStatus"],
        "season_game_postponed": True if raw_season_game_data["strPostponed"]=="yes" else False,
        "season_game_league_id": raw_season_game_data["idLeague"],
        }
    return parsed_season_game_data

leagues = {
           "MLB": {"league_id": "4424", "season": "2023"}, 
           "NFL": {"league_id": "4391", "season": "2023"},
           "NBA": {"league_id": "4387", "season": "2023-2024"},
           "NHL": {"league_id": "4380", "season" : "2023-2024"},
           }

sample_league_season_games = {}

for league, league_info in leagues.items():
        league_id = league_info["league_id"]
        league_season = league_info["season"]
        print(league, league_id, league_season)

        league_season_games_url = f"https://www.thesportsdb.com/api/v1/json/40130162/eventsseason.php?id={league_id}&s={league_season}"
        league_season_games_data = requests.get(league_season_games_url)
        league_season_games_dict = json.loads(league_season_games_data.text)
        league_season_games_example = league_season_games_dict["events"][0]
        sample_league_season_games[league] = league_season_games_example
        for k, v in league_season_games_example.items():
            print(k,v)
        print('---------------')

if sample_league_season_games["MLB"].keys() == sample_league_season_games["NFL"].keys() == sample_league_season_games["NBA"].keys() == sample_league_season_games["NHL"].keys():
        for league in leagues:
                print(league)
                parsed_player_data = parse_season_game_data(sample_league_season_games[league])
                for key, val in parsed_player_data.items():
                        print(key, val, type(val))
                print("-----------------------")
else:
        print('Keys are different')