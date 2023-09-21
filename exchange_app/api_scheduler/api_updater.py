from apscheduler.schedulers.background import BackgroundScheduler
from exchange_app.models import update_teams, update_season_games, update_live_games, update_upcoming_games
from datetime import datetime, timedelta
import time


leagues = {
           "MLB": {"league_id": "4424", "season": "2023"}, 
           "NFL": {"league_id": "4391", "season": "2023"},
           "NBA": {"league_id": "4387", "season": "2023-2024"},
           "NHL": {"league_id": "4380", "season": "2023-2024"},
           }


def start():
    scheduler = BackgroundScheduler()
    for league, info in leagues.items():
        # break
        # Fecth Team Info
        scheduler.add_job(update_teams, "interval", days=1, id=f"update_{league}_teams", args=[league], replace_existing=True, 
                      next_run_time=datetime.now())

        # # Backfill Season Games
        # scheduler.add_job(update_season_games, "interval", days=30, id=f"update_{league}_season_games", args=[info["league_id"], info["season"]], 
        #               replace_existing=True, next_run_time=datetime.now() + timedelta(minutes=0))
        
        # Fecth upcoming games data
        # scheduler.add_job(update_upcoming_games, "interval", hours=12, id=f"update_{league}_upcoming_games", args=[info["league_id"]], 
        #                 replace_existing=True, next_run_time=datetime.now() + timedelta(seconds=20))

        # Fetch live games data
        scheduler.add_job(update_live_games, "interval", seconds=30, id=f"update_{league}_live_games", args=[info["league_id"]], 
                      replace_existing=True, next_run_time=datetime.now() + timedelta(seconds=0))
        
    scheduler.start()
