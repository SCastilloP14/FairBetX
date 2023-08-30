import requests
import json
from datetime import datetime

def fetch_player_data(team_id):
    # Fetch games data and return list of players
    try:
        team_players_url = f"https://www.thesportsdb.com/api/v1/json/40130162/lookup_all_players.php?id={team_id}"
        team_players_data = requests.get(team_players_url)
        team_players_dict = json.loads(team_players_data.text)
        team_players_list = team_players_dict["player"]
        parsed_player_list = parse_players_data(team_players_list)
        return parsed_player_list
    except Exception as e:
        print(e)
        return []


def fetch_team_data(league_name):
    try:
        league_teams_url = f"https://www.thesportsdb.com/api/v1/json/3/search_all_teams.php?l={league_name}"
        league_teams_data = requests.get(league_teams_url)
        league_teams_dict = json.loads(league_teams_data.text)
        league_teams_list = league_teams_dict["teams"]
        parsed_teams_list = parse_teams_data(league_teams_list)
        return parsed_teams_list
    except Exception as e:
        print(e)
        return []


def fetch_season_games(league_id, season_str):
    try:
        season_games_url = f"https://www.thesportsdb.com/api/v1/json/40130162/eventsseason.php?id={league_id}&s={season_str}"
        print(season_games_url)
        season_games_data = requests.get(season_games_url)
        season_games_dict = json.loads(season_games_data.text)
        season_games_list = season_games_dict["events"]
        parsed_season_list = parse_season_games_data(season_games_list)
        return parsed_season_list
    except Exception as e:
        print(e)
        return []

def fetch_live_scores_data(league_id):
    # Fetch games data and return list of dicts
    try:
        live_games_url = f"https://www.thesportsdb.com/api/v2/json/40130162/livescore.php?l={league_id}"
        print(live_games_url)
        live_games_data = requests.get(live_games_url)
        live_games_dict = json.loads(live_games_data.text)
        live_games_list = live_games_dict["events"]
        parsed_live_games = parse_live_games_data(live_games_list)
        return parsed_live_games
    except Exception as e:
        print(e)
        return []
    
# ------------------- PARSE METHODS --------------------

def parse_players_data(raw_players_data):
    parsed_players_data = []
    for player in raw_players_data:
        parsed_player = {"name": player["strPlayer"],
                            "number": player["strNumber"],
                            "player_id": player["idPlayer"],
                            "team_id": player["idTeam"]
                            }
        parsed_players_data.append(parsed_player)
    return parsed_players_data

def parse_teams_data(raw_teams_list):
    parsed_teams_list = []
    for team in raw_teams_list:
        parsed_team = {"team_id": team["idTeam"],
                       "name": team["strTeam"],
                       "sport": team["strSport"],
                       "short_name": team["strTeamShort"],
                       "stadium": team["strStadium"],
                       "badge": team ["strTeamBadge"],
                       "jersey": team["strTeamJersey"],
                       "logo": team["strTeamLogo"]
                       }
        parsed_teams_list.append(parsed_team)
    return parsed_teams_list

def parse_season_games_data(raw_games_list):
    parsed_season_matches_data = []
    for game in raw_games_list:
        parsed_match = {"game_id": game["idEvent"],
                        "sport": game["strSport"],
                        "league": game["strLeague"],
                        "league_id": game["idLeague"],
                        "home_team_id": game["idHomeTeam"],
                        "away_team_id": game["idAwayTeam"],
                        "home_team_score": game["intHomeScore"],
                        "away_team_score": game["intAwayScore"],
                        "start_time": datetime.strptime(game["strTimestamp"], '%Y-%m-%dT%H:%M:%S%z'),
                        "status": game["strStatus"] if 'IN' not in game["strStatus"] else "IN",
                        }
        parsed_season_matches_data.append(parsed_match)
    return parsed_season_matches_data


def parse_live_games_data(raw_games_list):
    parsed_live_matches_data = []
    for game in raw_games_list:
        game_time_str = f"{game['dateEvent']}T{game['strEventTime']}:00+00:00"
        parsed_live_match = {"game_id": game["idEvent"],
                        "sport": game["strSport"],
                        "league": game["strLeague"],
                        "league_id": game["idLeague"],
                        "home_team_id": game["idHomeTeam"],
                        "away_team_id": game["idAwayTeam"],
                        "home_team_score": game["intHomeScore"],
                        "away_team_score": game["intAwayScore"],
                        "start_time": datetime.strptime(game_time_str, '%Y-%m-%dT%H:%M:%S%z'),
                        "progress": game["strProgress"],
                        "status": game["strStatus"] if 'IN' not in game["strStatus"] else "IN",
                        }
        parsed_live_matches_data.append(parsed_live_match)
    return parsed_live_matches_data
