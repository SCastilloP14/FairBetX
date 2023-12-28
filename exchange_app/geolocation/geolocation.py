import json
import requests


def get_location_from_ip(ip_address):
    print("searchinf gor ip", ip_address)
    location_url = f"http://ip-api.com/json/{ip_address}"
    location_data = requests.get(location_url)
    print(location_data)
    location_dict = json.loads(location_data.text)

    return location_dict

