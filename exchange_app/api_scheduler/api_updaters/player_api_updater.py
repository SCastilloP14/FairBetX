import json
import requests
from datetime import datetime, timezone
from exchange_app.models import Team, Player 



def fetch_player_data(team_id):
    try:
        team_players_url = f"https://www.thesportsdb.com/api/v1/json/40130162/lookup_all_players.php?id={team_id}"
        team_players_data = requests.get(team_players_url)
        team_players_dict = json.loads(team_players_data.text)
        team_players_list = team_players_dict["player"]
        if team_players_list:
            parsed_player_list = [parse_player_data(player_data) for player_data in team_players_list]
            return parsed_player_list
        else:
            return []
    except Exception as e:
        print(f"Error fetching player data for {team_id}:", e, team_players_url)
        return []
    
def parse_player_birthday(datetime_str):
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
        except:
            print("Failed", datetime_str)
            return None

def parse_player_data(raw_player_data):
    parsed_team_data = {
          "player_id": raw_player_data["idPlayer"],
          "player_team_id": raw_player_data["idTeam"],
          "player_nationality": raw_player_data["strNationality"],
          "player_name": raw_player_data["strPlayer"],
          "player_sport": raw_player_data["strSport"],
          "player_date_of_birth": parse_player_birthday(raw_player_data["dateBorn"]),
          "player_number": raw_player_data["strNumber"] if raw_player_data["strNumber"]!="" else None,
          "player_birth_location": raw_player_data["strBirthLocation"],
          "player_status": raw_player_data["strStatus"],
          "player_description": raw_player_data["strDescriptionEN"],
          "player_gender": raw_player_data["strGender"],
          "player_position": raw_player_data["strPosition"],
          "player_height": raw_player_data["strHeight"],
          "player_weight": raw_player_data["strWeight"],
          "player_photo": raw_player_data["strCutout"], 
          }
    return parsed_team_data

def update_players_data(team_id):
    print("Updating Players for:", team_id)
    parsed_player_data_list = fetch_player_data(team_id)
    for parsed_player_data in parsed_player_data_list:
        create_or_update_player(**parsed_player_data)

def update_player(existing_player: Player, **kwargs):
    try:
        existing_player_team = Team.objects.get(team_id=kwargs["player_team_id"])
        existing_player.player_name = kwargs["player_name"]
        existing_player.player_sport = kwargs["player_sport"]
        existing_player.player_nationality = kwargs["player_nationality"]
        existing_player.player_date_of_birth = kwargs["player_date_of_birth"]
        existing_player.player_number = kwargs["player_number"]
        existing_player.player_birth_location = kwargs["player_birth_location"]
        existing_player.player_status = kwargs["player_status"]
        existing_player.player_description = kwargs["player_description"]
        existing_player.player_gender = kwargs["player_gender"]
        existing_player.player_position = kwargs["player_position"]
        existing_player.player_height = kwargs["player_height"]
        existing_player.player_weight = kwargs["player_weight"]
        existing_player.player_photo = kwargs["player_photo"]
        existing_player.player_team = existing_player_team
    except Team.DoesNotExist as e:
        print(f"Team id {kwargs['player_team_id']} not found for player", e)

def create_player(**kwargs):
    try:
        new_player_team = Team.objects.get(team_id=kwargs["player_team_id"])
        new_object = Player(player_id=kwargs["player_id"], 
                            player_name=kwargs["player_name"],
                            player_sport=kwargs["player_sport"], 
                            player_nationality=kwargs["player_nationality"], 
                            player_date_of_birth=kwargs["player_date_of_birth"],  
                            player_number=kwargs["player_number"], 
                            player_birth_location=kwargs["player_birth_location"], 
                            player_status=kwargs["player_status"], 
                            # player_description=kwargs["player_description"][100], 
                            player_description="",
                            player_gender=kwargs["player_gender"], 
                            player_position=kwargs["player_position"], 
                            player_height=kwargs["player_height"], 
                            player_weight=kwargs["player_weight"], 
                            player_photo=kwargs["player_photo"], 
                            player_team=new_player_team)
        new_object.save()
    except Team.DoesNotExist as e:
        print(f"Team id {kwargs['player_team_id']} not found for player", e)

def create_or_update_player(**kwargs):
    try:
        exsisting_player = Player.objects.get(player_id=kwargs["player_id"])
        update_player(exsisting_player, **kwargs)
    except Player.DoesNotExist:
        create_player(**kwargs)

if "__main__" == __name__: 
    teams = Team.objects.filter()
    team_id_list = [team.team_id for team in teams]
    for team_id in team_id_list:
        update_players_data(team_id)