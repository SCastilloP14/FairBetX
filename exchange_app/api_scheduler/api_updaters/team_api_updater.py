
import json
import requests
from exchange_app.models import Team, League

def fetch_team_data(league_name):
    try:
        league_teams_url = f"https://www.thesportsdb.com/api/v1/json/3/search_all_teams.php?l={league_name}"
        league_teams_data = requests.get(league_teams_url)
        league_teams_dict = json.loads(league_teams_data.text)
        league_teams_list = league_teams_dict["teams"]
        if league_teams_list:
            parsed_teams_list = [parse_team_data(team_data) for team_data in league_teams_list]
            return parsed_teams_list
        else:
            return []
    except Exception as e:
        print(f"Error fetching team data for {league_name}:", e)
        return []

def parse_team_data(raw_team_data):
    parsed_team_data = {
        "team_id": raw_team_data["idTeam"],
        "team_name": raw_team_data["strTeam"],
        "team_short_name": raw_team_data["strTeamShort"],
        "team_year_formed": raw_team_data["intFormedYear"],
        "team_sport": raw_team_data["strSport"],
        "team_league_1_id": raw_team_data["idLeague"],
        "team_league_2_id": raw_team_data["idLeague2"],
        "team_league_3_id": raw_team_data["idLeague3"],
        "team_league_4_id": raw_team_data["idLeague4"],
        "team_league_5_id": raw_team_data["idLeague5"],
        "team_league_6_id": raw_team_data["idLeague6"],
        "team_league_7_id": raw_team_data["idLeague7"],
        "team_stadium": raw_team_data["strStadium"],
        "team_stadium_description": raw_team_data["strStadiumDescription"],
        "team_stadium_capacity": raw_team_data["intStadiumCapacity"] if raw_team_data["intStadiumCapacity"]!=0 else None,
        "team_location": raw_team_data["strStadiumLocation"],
        "team_country": raw_team_data["strCountry"],
        "team_gender": raw_team_data["strGender"],
        "team_description": raw_team_data["strDescriptionEN"],
        "team_badge": raw_team_data["strTeamBadge"],
        "team_jersey": raw_team_data["strTeamJersey"],
        "team_logo": raw_team_data["strTeamLogo"]
        }
    return parsed_team_data

def updated_team_data(league_name):
    print("Updating Teams for:", league_name)
    parsed_team_data_list = fetch_team_data(league_name)
    for parsed_team_data in parsed_team_data_list:
        create_or_update_team(**parsed_team_data)
     
def update_team(existing_team: Team, **kwargs):
    existing_team.team_name = kwargs["team_name"]
    existing_team.team_short_name = kwargs["team_short_name"]
    existing_team.team_year_formed = kwargs["team_year_formed"]
    existing_team.team_sport = kwargs["team_sport"]
    existing_team.team_league_1 = kwargs["team_league_1"]
    existing_team.team_league_2 = kwargs["team_league_2"]
    existing_team.team_league_3 = kwargs["team_league_3"]
    existing_team.team_league_4 = kwargs["team_league_4"]
    existing_team.team_league_5 = kwargs["team_league_5"]
    existing_team.team_league_6 = kwargs["team_league_6"]
    existing_team.team_league_7 = kwargs["team_league_7"]
    existing_team.team_stadium = kwargs["team_stadium"]
    existing_team.team_stadium_description = kwargs["team_stadium_description"]
    existing_team.team_stadium_capacity = kwargs["team_stadium_capacity"]
    existing_team.team_location = kwargs["team_location"]
    existing_team.team_country = kwargs["team_country"]
    existing_team.team_gender = kwargs["team_gender"]
    existing_team.team_description = kwargs["team_description"]
    existing_team.team_badge = kwargs["team_badge"]
    existing_team.team_jersey = kwargs["team_jersey"]
    existing_team.team_logo = kwargs["team_logo"]
    existing_team.save()

def create_team(**kwargs):
    new_team = Team(team_id=kwargs["team_id"], 
                    team_name=kwargs["team_name"], 
                    team_short_name=kwargs["team_short_name"], 
                    team_year_formed=kwargs["team_year_formed"], 
                    team_sport=kwargs["team_sport"], 
                    team_league_1=kwargs["team_league_1"], 
                    team_league_2=kwargs["team_league_2"], 
                    team_league_3=kwargs["team_league_3"], 
                    team_league_4=kwargs["team_league_4"], 
                    team_league_5=kwargs["team_league_5"], 
                    team_league_6=kwargs["team_league_6"], 
                    team_league_7=kwargs["team_league_7"], 
                    team_stadium=kwargs["team_stadium"], 
                    team_stadium_description=kwargs["team_stadium_description"], 
                    team_stadium_capacity=kwargs["team_stadium_capacity"], 
                    team_location=kwargs["team_location"], 
                    team_country=kwargs["team_country"], 
                    team_gender=kwargs["team_gender"], 
                    team_description=kwargs["team_description"], 
                    team_badge=kwargs["team_badge"], 
                    team_jersey=kwargs["team_jersey"], 
                    team_logo=kwargs["team_logo"], 
                    )
    new_team.save()


def create_or_update_team(**kwargs):
    # There are 7 leagues per team on the API
    leagues_range = range(1,8)
    for n in leagues_range:
        if kwargs[f"team_league_{n}_id"]:
            try:
                kwargs[f"team_league_{n}"] = League.objects.get(league_id=kwargs[f"team_league_{n}_id"])
            except League.DoesNotExist as e:
                kwargs[f"team_league_{n}"] = None
        else:
            kwargs[f"team_league_{n}"] = None
    try:
        exsiting_team = Team.objects.get(team_id=kwargs["team_id"])
        update_team(exsiting_team, **kwargs)
    except Team.DoesNotExist:
        create_team(**kwargs)

def fetch_league_list():
    leagues = League.objects.filter()
    league_names = [league.league_name for league in leagues]
    return league_names


if "__main__" == __name__:
    leagues = League.objects.filter()
    league_names = [league.league_name for league in leagues]
    for league_name in league_names:
        updated_team_data(league_name)