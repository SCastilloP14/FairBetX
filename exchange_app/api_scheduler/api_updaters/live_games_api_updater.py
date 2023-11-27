
import requests
import json
from datetime import datetime, timezone, timedelta
from exchange_app.models import Game, Ticker, League, GameStatus, game_status_mapping, ticker_status_mapping


def fetch_live_games_data(league_id):
    # Fetch games data and return list of dicts
    try:
        live_games_url = f"https://www.thesportsdb.com/api/v2/json/40130162/livescore.php?l={league_id}"
        live_games_data = requests.get(live_games_url)
        live_games_dict = json.loads(live_games_data.text)
        live_games_list = live_games_dict["events"]
        if live_games_list:
            unique_statuses = {d["strStatus"] for d in live_games_list}
            print(unique_statuses)
            parsed_live_games = [parse_live_game_data(live_game_data) for live_game_data in live_games_list]
            return parsed_live_games
        else:
            return []
    except Exception as e:
        print(f"Error fetching live scores data for {league_id}", e)
        return []
    
def parse_game_datetime(datetime_str):
        try:
            if "+" in datetime_str:
                parsed_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
            elif "-" in datetime_str and ":" not in datetime_str:
                parsed_datetime = datetime.strptime(datetime_str, '%Y-%m-%d').replace(tzinfo=timezone.utc)
            elif ":" in datetime_str:
                parsed_datetime = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S').astimezone(timezone.utc)
            else:
                parsed_datetime = datetime.utcfromtimestamp(int(datetime_str)).replace(tzinfo=timezone.utc)
            return parsed_datetime
        except Exception as e:
            print("Failed parsing live game date", datetime_str, e)
            return None
    
def parse_live_game_data(raw_live_game_data):
    parsed_live_game_data = {
        "live_game_id": raw_live_game_data["idEvent"],
        "live_game_home_team_score": raw_live_game_data["intHomeScore"],
        "live_game_away_team_score": raw_live_game_data["intAwayScore"],
        "live_game_status": game_status_mapping.get(raw_live_game_data["strStatus"], GameStatus.PLAYING.name) if raw_live_game_data["strStatus"]!="" else game_status_mapping.get(raw_live_game_data["strProgress"], GameStatus.PLAYING.name),       
        "live_game_progress": raw_live_game_data["strProgress"]
        }
    return parsed_live_game_data

def update_live_game_data(league_id,):
    print("Updating Live games for:", league_id)
    parsed_live_game_data_list = fetch_live_games_data(league_id)
    for parsed_live_game_data in parsed_live_game_data_list:
        update_live_game(**parsed_live_game_data)

def create_ticker(game: Game):
    if game.game_start_datetime and game.game_start_datetime > datetime.now().astimezone(timezone.utc) - timedelta(hours=3) and game.game_start_datetime < datetime.now().astimezone(timezone.utc) + timedelta(days=7):
            try:
                Ticker.objects.get(ticker_id=f"{game.game_id}-T")
                print("Tciker already created")
            except Ticker.DoesNotExist:
                new_ticker = Ticker(ticker_id=f"{game.game_id}-T",
                                    ticker_game=game,
                                    ticker_status=ticker_status_mapping.get(game.game_status)
                                    )
                new_ticker.save()

def update_live_game(**kwargs):
    try:
        existing_game = Game.objects.get(game_id=kwargs["live_game_id"])
        existing_game.game_home_team_score = kwargs["live_game_home_team_score"]
        existing_game.game_away_team_score = kwargs["live_game_away_team_score"]
        existing_game.game_status = kwargs["live_game_status"]
        existing_game.game_progress = kwargs["live_game_progress"]
        existing_game.save()
        existing_ticker = Ticker.objects.get(ticker_game=existing_game)
        if existing_game.game_status == GameStatus.PLAYING.name:
            if kwargs["live_game_status"] == GameStatus.FINISHED.name:
                existing_ticker.close_ticker()
            elif kwargs["live_game_status"] == GameStatus.POSTPONED.name or kwargs["live_game_status"] == GameStatus.CANCELED.name or kwargs["live_game_status"] == GameStatus.ABDANDONED.name:
                existing_ticker.cancel_ticker()
        elif existing_game.game_status == GameStatus.SCHEDULED.name:
            if kwargs["live_game_status"] == GameStatus.POSTPONED.name or kwargs["live_game_status"] == GameStatus.CANCELED.name or kwargs["live_game_status"] == GameStatus.ABDANDONED.name:
                existing_ticker.cancel_ticker()
    except Ticker.DoesNotExist:
        existing_game = Game.objects.get(game_id=kwargs["live_game_id"])
        create_ticker(existing_game)
    except Game.DoesNotExist:
        print(f"Missing a team for game {kwargs['live_game_id']}:", kwargs["season_game_home_team_id"], kwargs["season_game_away_team_id"])

if "__main__" == __name__: 
    leagues = League.objects.filter()
    league_names = [league.league_name for league in leagues]
    for league_name in league_names:
        update_live_game_data(league_name)