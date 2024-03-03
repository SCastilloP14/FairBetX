import json
import requests
from exchange_app.models import League, Team


def fetch_league_data(league_id):
    try:
        league_details_url = f"https://www.thesportsdb.com/api/v1/json/40130162/lookupleague.php?id={league_id}"
        league_details_data = requests.get(league_details_url)
        league_details_dict = json.loads(league_details_data.text)
        league_details_list = league_details_dict["leagues"]
        if league_details_list:
            parsed_league_list = [parse_league_data(league_detail) for league_detail in league_details_list]
            return parsed_league_list
        else:
            return []
    except Exception as e:
        print(f"Error fetching league data for {league_id}:", e)
        return []
    
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
        "league_trophy": raw_team_data["strTrophy"],
    }
    return parsed_league_data

def updated_league_data(league_name):
    print("Updating League:", league_name)
    parsed_league_data_list = fetch_league_data(league_name)
    for parsed_league_data in parsed_league_data_list:
        create_or_update_league(**parsed_league_data)


def update_league(existing_league: League, **kwargs):
        existing_league.league_sport = kwargs["league_sport"]
        existing_league.league_name = kwargs["league_name"]
        existing_league.league_alternative_name = kwargs["league_alternative_name"]
        existing_league.league_current_season = kwargs["league_current_season"]
        existing_league.league_formed_year = kwargs["league_formed_year"]
        existing_league.league_first_event = kwargs["league_first_event"]
        existing_league.league_gender = kwargs["league_gender"]
        existing_league.league_country = kwargs["league_country"]
        existing_league.league_description = kwargs["league_description"]
        existing_league.league_badge = kwargs["league_badge"]
        existing_league.league_logo = kwargs["league_logo"]
        existing_league.league_trophy = kwargs["league_trophy"]
        existing_league.save()

def create_league(**kwargs):
    print("creating_league")
    new_league = League(league_id=kwargs["league_id"],
                        league_sport=kwargs["league_sport"],
                        league_name=kwargs["league_name"],
                        league_alternative_name=kwargs["league_alternative_name"],
                        league_current_season = kwargs["league_current_season"],
                        league_formed_year=kwargs["league_formed_year"],
                        league_first_event=kwargs["league_first_event"],
                        league_gender=kwargs["league_gender"],
                        league_country=kwargs["league_country"],
                        league_description=kwargs["league_description"],
                        league_badge=kwargs["league_badge"],
                        league_logo=kwargs["league_logo"],
                        league_trophy=kwargs["league_trophy"])
    new_league.save()

def create_or_update_league(**kwargs):
    try:
        league = League.objects.get(league_id=kwargs["league_id"])
        update_league(league, **kwargs)
    except League.DoesNotExist:
        create_league(**kwargs)


if "__main__" == __name__: 
    leagues =["MLB", "NBA", "NFL", "NHL"]
    for league in leagues:
        updated_league_data(league)