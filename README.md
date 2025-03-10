## Movide Query Batch Generator

**This tool is untested on a larger scale, as the MOTIS demo was not available at the time of writing.**

### What is the Query Batch generator?

This tool is used to automatically build larger query batches used to test MOTIS with the Motis Visual Debugger.

The Python tool allows for larger-scale automated generation of queries that can be directly inserted into MoViDe and be used to test larger sets of data and more diverse routes.

The query batch generator takes two random cities from a preselected dataset (see more in the section _input data_), gets their latitude and longitude, as well as the level and stop ID from Motis' API, and puts them into the data format that MoViDe expects. 

##### Note:
To diversify the queries even further, the query batch generator randomizes the queries from a given start point to where in the next 7 days following the start point.

Example:
- **Given start date:** 2025-03-10T15:00:00Z
- **Latest possible query start:** 2025-03-17T15:00:00Z

### Using the Query batch generator

The query batch generator has five different command line flags:

- **cities**
    - path to the input dataset, which holds the cities and their geolocation
    - default: ./cities.json
- **queries**
    - path to the query batch file, holding the generated queries
    - default: ./query-batch.json
- **amount**
    - the number of queries that should be generated
    - default: 10
- **time**
    - the date in ISO8601 format for when the queries should be dated
    - default: current time
- **motis-url**
    - the URL that the motis instance that should be tested runs at
    - default: http://localhost:8080/

### Installation/Requirements: 

1. Install the ``requests`` Python package.
2. Download the geolocation dataset, which holds the information for the cities.
    - ``wget https://raw.githubusercontent.com/idris-maps/map-of-europe/refs/heads/master/data/cities.json``

