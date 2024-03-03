import json
import requests
from datetime import datetime, timezone, timedelta
from exchange_app.models import Game, Team, League, Ticker, GameStatus, TickerStatus, game_status_mapping, ticker_status_mapping


def fetch_season_games(league_id, season_str):
    try:
        season_games_url = f"https://www.thesportsdb.com/api/v1/json/40130162/eventsseason.php?id={league_id}&s={season_str}"
        season_games_data = requests.get(season_games_url)
        season_games_dict = json.loads(season_games_data.text)
        season_games_list = season_games_dict["events"]
        if season_games_list:
            parsed_season_list = [parse_season_game_data(season_game_data) for season_game_data in season_games_list]
            return parsed_season_list
        else:
            return []
    except Exception as e:
        print(f"Error fetching season data for {league_id} {season_str}:", e)
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
            print("Failed parsing season game date", datetime_str, e)
            return None


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
        "season_game_status": game_status_mapping.get(raw_season_game_data["strStatus"], GameStatus.PLAYING.name),
        "season_game_postponed": True if raw_season_game_data["strPostponed"]=="yes" else False,
        "season_game_progress": "",
        "season_game_league_id": raw_season_game_data["idLeague"],
        }
    return parsed_season_game_data

def update_season_game_data(league_id, league_season):
    print("Updating Season games for:", league_id, league_season)
    parsed_season_game_data_list = fetch_season_games(league_id, league_season)
    for parsed_season_game_data in parsed_season_game_data_list:
        create_or_update_season_game(**parsed_season_game_data)

def update_season_game(existing_game: Game, **kwargs):
    existing_game.game_name = kwargs["season_game_name"]
    existing_game.game_alternative_name = kwargs["season_game_alternative_name"]
    existing_game.game_filename = kwargs["season_game_filename"]
    existing_game.game_season = kwargs["season_game_season"]
    existing_game.game_home_team_score = kwargs["season_game_home_team_score"]
    existing_game.game_away_team_score = kwargs["season_game_away_team_score"]
    existing_game.game_round = kwargs["season_game_round"]
    existing_game.game_spectators = kwargs["season_game_spectators"]
    existing_game.game_official = kwargs["season_game_official"]
    existing_game.game_start_datetime = kwargs["season_game_start_datetime"]
    existing_game.game_results = kwargs["season_game_results"]
    existing_game.game_venue = kwargs["season_game_venue"]
    existing_game.game_country = kwargs["season_game_country"]
    existing_game.game_city = kwargs["season_game_city"]
    existing_game.game_status = kwargs["season_game_status"]
    existing_game.game_postponed = kwargs["season_game_postponed"]
    existing_game.save()

    try:
        if Ticker.objects.filter(ticker_id=f"{existing_game.game_id}-T"):
            existing_ticker = Ticker.objects.get(ticker_id=f"{existing_game.game_id}-T")
            if existing_ticker.ticker_status == TickerStatus.OPEN.name and ticker_status_mapping.get(existing_game.game_status) != TickerStatus.OPEN.name:
                if ticker_status_mapping.get(existing_game.game_status) == TickerStatus.CLOSED.name:
                    existing_ticker.close_ticker()
                elif ticker_status_mapping.get(existing_game.game_status) == TickerStatus.CANCELED.name:
                    existing_ticker.cancel_ticker
        else:
            create_ticker(existing_game)
    except Ticker.DoesNotExist:
        create_ticker(existing_game)
    

def create_season_game(**kwargs):
    try:
        game_home_team = Team.objects.get(team_id=kwargs["season_game_home_team_id"])
        game_away_team=Team.objects.get(team_id=kwargs["season_game_away_team_id"]) 
        game_league = League.objects.get(league_id=kwargs["season_game_league_id"])
        new_game = Game(game_id=kwargs["season_game_id"], 
                        game_name=kwargs["season_game_name"],
                        game_alternative_name=kwargs["season_game_alternative_name"],
                        game_filename=kwargs["season_game_filename"],
                        game_season=kwargs["season_game_season"],
                        game_home_team=game_home_team,
                        game_away_team=game_away_team,
                        game_home_team_score=kwargs["season_game_home_team_score"],
                        game_away_team_score=kwargs["season_game_away_team_score"],
                        game_round=kwargs["season_game_round"],
                        game_spectators=kwargs["season_game_spectators"],
                        game_official=kwargs["season_game_official"],
                        game_start_datetime=kwargs["season_game_start_datetime"],
                        game_results=kwargs["season_game_results"],
                        game_venue=kwargs["season_game_venue"],
                        game_country=kwargs["season_game_country"],
                        game_city=kwargs["season_game_city"],
                        game_status=kwargs["season_game_status"],
                        game_postponed=kwargs["season_game_postponed"],
                        game_league=game_league,
                        )
        new_game.save()
        create_ticker(new_game)
    except Team.DoesNotExist as e:
        print(f"Team id {kwargs['season_game_home_team_id']} : {kwargs['season_game_away_team_id']} nopt found for game {kwargs['game_id']}", e)
    except League.DoesNotExist as e:
        print(f"League id {kwargs['season_game_league_id']} not found for game {kwargs['season_game_id']}", e)


def create_or_update_season_game(**kwargs):
    try:
        existing_game = Game.objects.get(game_id=kwargs["season_game_id"])
        update_season_game(existing_game, **kwargs)
    except Game.DoesNotExist:
        try:
             if datetime.now().astimezone(timezone.utc) - timedelta(days=1) < kwargs['season_game_start_datetime'] < datetime.now().astimezone(timezone.utc) + timedelta(days=10):
                print(f"Creating game for {kwargs['season_game_filename']}")
                create_season_game(**kwargs)         
        except Team.DoesNotExist:
            print(f"Missing a team for game {kwargs['season_game_id']}:", kwargs["season_game_home_team_id"], kwargs["season_game_away_team_id"])


def create_ticker(game: Game):
    if game.game_status != GameStatus.NO_STATUS.name:
        if game.game_start_datetime:
            if datetime.now().astimezone(timezone.utc) - timedelta(hours=3) < game.game_start_datetime < datetime.now().astimezone(timezone.utc) + timedelta(days=7):
                try:
                    Ticker.objects.get(ticker_id=f"TICK-{game.game_id}")
                except Ticker.DoesNotExist:
                    print(f"Creating ticker for game {game.game_filename}")
                    new_ticker = Ticker(ticker_id=f"TICK-{game.game_id}",
                                        ticker_game=game,
                                        ticker_status=ticker_status_mapping.get(game.game_status)
                                        )
                    new_ticker.save()

if "__main__" == __name__: 
    leagues = League.objects.filter()
    leagues_details = [{"league_id": league.league_id,
                        "league_season": league.league_current_season
                        } for league in leagues]
    for league in leagues_details:
        league_id = league["league_id"]
        league_season = league["league_season"]
        update_season_game_data(league_id, league_season)