from apscheduler.schedulers.background import BackgroundScheduler
from exchange_app.models import update_teams, update_season_games, update_live_games
from datetime import datetime, timedelta


def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(update_teams, "interval", days=1, id="update_MLB_teams", args=["MLB"], replace_existing=True, 
    #                   next_run_time=datetime.now())
    # scheduler.add_job(update_teams, "interval", days=1, id="update_NBA_teams", args=["NBA"], replace_existing=True, 
    #                   next_run_time=datetime.now())
    # scheduler.add_job(update_teams, "interval", days=1, id="update_NFL_teams", args=["NFL"], replace_existing=True, 
    #                   next_run_time=datetime.now())
    
    # scheduler.add_job(update_season_games, "interval", days=30, id="update_MLB_season_games", args=["4424", "2023"], 
    #                   replace_existing=True, next_run_time=datetime.now() + timedelta(minutes=0))
    
    # scheduler.add_job(update_live_games, "interval", minutes=1, id="update_MLB_live_games", args=["4424"], 
    #                   replace_existing=True, next_run_time=datetime.now() + timedelta(minutes=0))
    

    scheduler.start()
