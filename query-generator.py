import json
import argparse
import random
import copy
from datetime import datetime,timedelta
import re
import requests
import module
    
def parse_json(path_to_file):
    args = module.build_arguments()
    file = open(path_to_file, "r").read()
    return json.loads(file)

def iso8601_to_microseconds(iso_string):
    # Regex to parse ISO 8601 format
    pattern = r"(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?(?:Z|([+-]\d{2}):?(\d{2}))?"
    match = re.match(pattern, iso_string)
    
    if not match:
        raise ValueError("Invalid ISO 8601 format")
    
    # Extract components
    year, month, day = map(int, match.group(1, 2, 3))
    hour, minute, second = map(int, match.group(4, 5, 6))
    microsecond = int(match.group(7) or 0)  # Default to 0 if no fractional seconds
    tz_sign = match.group(8)
    tz_hour = int(match.group(9) or 0) if tz_sign else 0
    tz_minute = int(match.group(10) or 0) if tz_sign else 0
    
    # Create naive datetime object
    dt = datetime(year, month, day, hour, minute, second, microsecond)
    
    # Adjust for timezone offset if present
    if tz_sign:
        offset = timedelta(hours=tz_hour, minutes=tz_minute)
        if tz_sign.startswith('-'):
            dt += offset
        else:
            dt -= offset
    
    # Convert to microseconds since epoch
    epoch = datetime(1970, 1, 1)
    delta = dt - epoch
    return int(delta.total_seconds() * 1_000_000 + delta.microseconds)

def microseconds_to_iso8601(microseconds_str):
    microseconds = int(microseconds_str)
    epoch = datetime(1970, 1, 1)
    dt = epoch + timedelta(microseconds=microseconds)
    return dt.isoformat()[:19] + 'Z'


def build_time(time):
    # if no time given get the current time
    if(time == "NO-TIME-GIVEN"):
        time = datetime.now()
        time = time.isoformat()
    
    time = iso8601_to_microseconds(time)
    
    offset = random.randint(0,604800000000)
    time = str(offset+time)
    
    return microseconds_to_iso8601(time)

def interpolate_template(index,template,cities,time):
    # generate start stop
    from_index = random.randint(0,363)

    # set index
    template["index"] = index

    # build start
    template = build_stop(from_index,template,cities,"from")
    
    # generate end stop
    to_index = random.randint(0,363)
    template = build_stop(to_index,template,cities,"to")
    
    # set time
    template["time"] = build_time(time)
    
    return template
   
def get_level_from_motis(location):
    url = "http://localhost:8080/api/v1/geocode/?text={location}"
    api_response = requests.get(url)
    json_data = json.loads(api_response.content)
    
    if (json_data == []):
        return ["ERROR OCCURED IN MOTIS API CALL","ERROR OCCURED IN MOTIS API CALL"]
    
    return_list = []
    return_list.append(json_data[0]["level"])
    return_list.append(json_data[0]["id"])

    return return_list


def build_stop(index,template,cities,stop):
     # set name
    template[stop]["name"] = cities["features"][index]["properties"]["name"]

    # set coordinates
    template[stop]["latitude"] = cities["features"][index]["geometry"]["coordinates"][0]
    template[stop]["longitude"] = cities["features"][index]["geometry"]["coordinates"][1]
    
    # set level
    motis_arguments =  get_level_from_motis(template[stop]["name"])

    if isinstance(motis_arguments[0],int):
        template[stop]["level"] = int(motis_arguments[0])
    template[stop]["stopId"] = motis_arguments[1]
    
    return template

def write_to_file(content,path):
    file = open(path,"w")
    file.write(content)
    file.close()

def main():
    args = module.build_arguments()
    cities = parse_json(args.cities)
    template = parse_json("./query-template.json")
    
    queries = []
    
    for i in range(args.amount):
        clone = copy.deepcopy(template)
        interpolated_template = interpolate_template(i,clone,cities,args.time)
        queries.append(interpolated_template)
    
    string_content = json.dumps(queries)
    write_to_file(string_content,args.queries)
    
main()