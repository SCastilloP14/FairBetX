from apscheduler.schedulers.background import BackgroundScheduler
from .api_updaters.league_api_updater import updated_league_data
from .api_updaters.team_api_updater import updated_team_data
from .api_updaters.player_api_updater import update_players_data
from .api_updaters.season_games_api_updater import update_season_game_data
from .api_updaters.live_games_api_updater import update_live_game_data
from datetime import datetime, timedelta
import time
from exchange_app.models import League, Team, Player, Game



def start():
    leagues = {
           "MLB": {"league_id": "4424", "season": "2023"}, 
           "NFL": {"league_id": "4391", "season": "2023"},
           "NBA": {"league_id": "4387", "season": "2023-2024"},
           "NHL": {"league_id": "4380", "season": "2023-2024"},
           }
    scheduler = BackgroundScheduler()
    print(datetime.now())
    for league, info in leagues.items():
        updated_league_data(info['league_id'])

    print(datetime.now())
    leagues = League.objects.filter()
    league_names = [league.league_name for league in leagues]
    for league_name in league_names:
        updated_team_data(league_name)

    print(datetime.now())  
    teams = Team.objects.filter()
    team_id_list = [team.team_id for team in teams]
    for team_id in team_id_list:
        update_players_data(team_id)
    
    print(datetime.now())
    leagues = League.objects.filter()
    leagues_details = [{"league_id": league.league_id,
                        "league_season": league.league_current_season
                        } for league in leagues]
    for league in leagues_details:
        league_id = league["league_id"]
        league_season = league["league_season"]
        update_season_game_data(league_id, league_season)

    print(datetime.now())
    leagues = League.objects.filter()
    league_ids = [league.league_id for league in leagues]
    for league_id in league_ids:
        update_live_game_data(league_id)
        scheduler.add_job(update_live_game_data, "interval", days=1, id=f"update_{league_id}_live_games", args=[league_id], replace_existing=True, 
                      next_run_time=datetime.now() + timedelta(seconds=30))

    print(datetime.now())

    scheduler.start()