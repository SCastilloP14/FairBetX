import requests
import json
from datetime import datetime



def parse_player_data(raw_player_data):
    parsed_team_data = {
          "player_id": raw_player_data["idPlayer"],
          "player_team_id": raw_player_data["idTeam"],
          "player_nationality": raw_player_data["strNationality"],
          "player_name": raw_player_data["strPlayer"],
          "player_sport": raw_player_data["strSport"],
          "player_date_of_birth": datetime.strptime(raw_player_data["dateBorn"], '%Y-%m-%d'),
          "player_number": raw_player_data["strNumber"],
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

teams = ["134880", "135267", "134946", "134846"]
sample_team_players = {}


for team_id in teams:
        team_players_url = f"https://www.thesportsdb.com/api/v1/json/40130162/lookup_all_players.php?id={team_id}"
        team_players_data = requests.get(team_players_url)
        team_players_dict = json.loads(team_players_data.text)
        team_player_example = team_players_dict["player"][0]
        sample_team_players[team_id] = team_player_example
        for k, v in team_player_example.items():
            print(k,v)
        print('---------------')

if sample_team_players["134880"].keys() == sample_team_players["135267"].keys() == sample_team_players["134946"].keys() == sample_team_players["134846"].keys():
        for team_id in teams:
                print(team_id)
                parsed_player_data = parse_player_data(sample_team_players[team_id])
                for key, val in parsed_player_data.items():
                        print(key, val, type(val))
                print("-----------------------")
else:
        print('Keys are different')