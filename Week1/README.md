# Week 1
**Question 1. Understanding docker first run:**
**- Run docker in intractive mode:**
docker run -it --entrypoint=bash python:3.12.8
**- To get the PIP version:**
pip --version 

**Question 2. Docker networking and docker-compose:**
-- Build the image:
docker build -t ingest_green_tripdata:v001 .
-- Run the image: 
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
lookup_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

docker run -it \
    --network=week1_default\
    ingest_green_tripdata:v001 \
    --user=postgres \
    --password=postgres \
    --host=db \
    --port=5432 \
    --database=ny_taxi \
    --table=green_taxi_trips \
    --lookup_table=taxi_zone \
    --url=${URL} \
    --lookup_url=${lookup_url} 