import json
import requests

def get_stop_from_motis(location,motis_URL):
    url = motis_URL+"api/v1/geocode/?text={location}"

    api_response = requests.get(url)
    json_data = json.loads(api_response.content)
    
    if (json_data == []):
        return ["ERROR OCCURED IN MOTIS API CALL","ERROR OCCURED IN MOTIS API CALL"]
    
    return_list = []
    return_list.append(json_data[0]["level"])
    return_list.append(json_data[0]["id"])

    return return_list