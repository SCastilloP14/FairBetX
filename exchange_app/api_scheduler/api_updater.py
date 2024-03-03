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
           "MLB": {"league_id": "4424"}, 
           "NFL": {"league_id": "4391"},
           "NBA": {"league_id": "4387"},
           "NHL": {"league_id": "4380"},
           }
    scheduler = BackgroundScheduler()
    print(datetime.now())

    # Update Legue data
    for league, info in leagues.items():
        league_id = info['league_id']
        updated_league_data(league_id)
        scheduler.add_job(updated_league_data, "interval", hours=24, id=f"update_{league_id}_data", args=[league_id], replace_existing=True, 
                      next_run_time=datetime.now() + timedelta(hours=2))

    leagues = League.objects.filter()
    league_names = [league.league_name for league in leagues]
    league_ids = [league.league_id for league in leagues]

    for league_name in league_names:
        scheduler.add_job(updated_team_data, "interval", hours=24, id=f"update_{league_name}_team_data", args=[league_name], replace_existing=True, 
                      next_run_time=datetime.now() + timedelta(hours=2))

    teams = Team.objects.filter()
    team_id_list = [team.team_id for team in teams]
    # for team_id in team_id_list:
    #     update_players_data(team_id)
    
    leagues = League.objects.filter()
    leagues_details = [{"league_id": league.league_id,
                        "league_current_season": league.league_current_season
                        } for league in leagues]
        
    for league in leagues_details:
        league_id = league["league_id"]
        league_current_season = league["league_current_season"]
        update_season_game_data(league_id, league_current_season)
        scheduler.add_job(update_season_game_data, "interval", hours=2, id=f"update_{league_id}_season_games", args=[league_id, league_current_season], replace_existing=True, 
                      next_run_time=datetime.now() + timedelta(hours=1))

    for league_id in league_ids:
        scheduler.add_job(update_live_game_data, "interval", seconds=30, id=f"update_{league_id}_live_games", args=[league_id], replace_existing=True, 
                      next_run_time=datetime.now())

    print(datetime.now())

    scheduler.start()