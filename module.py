import argparse

def build_arguments():
    parser = argparse.ArgumentParser(description='Script so useful.')
    parser.add_argument("--cities", type=str, default="./cities.json")
    parser.add_argument("--queries", type=str, default="./query-batch.json")
    parser.add_argument("--amount", type=int,default=10)
    parser.add_argument("--time", type=str, default="NO-TIME-GIVEN")
    parser.add_argument("--motis-url", type=str, default="http://localhost:8080/")

    return parser.parse_args()