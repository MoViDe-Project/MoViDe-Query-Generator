import json
import argparse
import random
import copy
from datetime import datetime

# module imports
import format_conversion
import motis_interaction

def build_time(time):
    # if no time given get the current time
    if(time == "NO-TIME-GIVEN"):
        time = datetime.now()
        time = time.isoformat()
    
    # prepare time format for randomization
    time = format_conversion.iso8601_to_microseconds(time)
    
    # randomize time field to somewhere in the next week
    offset = random.randint(0,604800000000)
    time = str(offset+time)
    
    return format_conversion.microseconds_to_iso8601(time)

def interpolate_template(index,template,cities,time,motis_URL):
    # generate start stop
    from_index = random.randint(0,363)

    # set index
    template["index"] = index

    # build start
    template = build_stop(from_index,template,cities,"from",motis_URL)
    
    # generate end stop
    to_index = random.randint(0,363)
    template = build_stop(to_index,template,cities,"to",motis_URL)
    
    # set time
    template["time"] = build_time(time)
    
    return template


def build_stop(index,template,cities,stop,motis_URL):
     # set name
    template[stop]["name"] = cities["features"][index]["properties"]["name"]

    # set coordinates
    template[stop]["latitude"] = cities["features"][index]["geometry"]["coordinates"][0]
    template[stop]["longitude"] = cities["features"][index]["geometry"]["coordinates"][1]
    
    # get level and stopId
    motis_arguments =  motis_interaction.get_stop_from_motis(template[stop]["name"],motis_URL)

    # if level and stopId retrieval were successful, set the template fields
    if isinstance(motis_arguments[0],int):
        template[stop]["level"] = int(motis_arguments[0])
    template[stop]["stopId"] = motis_arguments[1]
    
    return template

# file handling
def parse_json(path_to_file):
    file = open(path_to_file, "r").read()
    return json.loads(file)

def write_to_file(content,path):
    file = open(path,"w")
    file.write(content)
    file.close()

# parsing commandline flags and default values
def build_arguments():
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("--cities", type=str, default="./cities.json")
    parser.add_argument("--queries", type=str, default="./query-batch.json")
    parser.add_argument("--amount", type=int,default=10)
    parser.add_argument("--time", type=str, default="NO-TIME-GIVEN")
    parser.add_argument("--motisURL", type=str, default="http://localhost:8080/")

    return parser.parse_args()

def main():
    args = build_arguments()

    cities = parse_json(args.cities)
    template = parse_json("./query-template.json")
    
    queries = []
    
    for i in range(args.amount):
        clone = copy.deepcopy(template)
        interpolated_template = interpolate_template(i,clone,cities,args.time,args.motisURL)
        queries.append(interpolated_template)
    
    string_content = json.dumps(queries)
    write_to_file(string_content,args.queries)
    
main()