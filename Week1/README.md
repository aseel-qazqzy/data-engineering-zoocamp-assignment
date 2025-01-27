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


-- PGCLI to connet to the db 
pgcli -h localhost -p 5434 -u postgres -d ny_taxi

**Question 3. Trip Segmentation Count:**
During the period of October 1st 2019 (inclusive) and November 1st 2019 (exclusive), how many trips, respectively, happened:
Up to 1 mile
In between 1 (exclusive) and 3 miles (inclusive),
In between 3 (exclusive) and 7 miles (inclusive),
In between 7 (exclusive) and 10 miles (inclusive),
Over 10 miles

**Queries 1:**
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'green_taxi_trips';
SELECT
     SUM(CASE WHEN trip_distance <= 1 THEN 1 ELSE 0 END) AS up_to_1_mile,
     SUM(CASE WHEN trip_distance > 1 AND trip_distance <= 3 THEN 1 ELSE 0 END) AS between_1_and_3_miles,
     SUM(CASE WHEN trip_distance > 3 AND trip_distance <= 7 THEN 1 ELSE 0 END) AS between_3_and_7_miles,
     SUM(CASE WHEN trip_distance > 7 AND trip_distance <= 10 THEN 1 ELSE 0 END) AS between_7_and_10_miles,
     SUM(CASE WHEN trip_distance > 10 THEN 1 ELSE 0 END) AS over_10_miles
 FROM
     green_taxi_trips
 WHERE
     lpep_pickup_datetime >= '2019-10-01' AND lpep_pickup_datetime < '2019-11-01';

**Question 4:**
select max(trip_distance) as max_distance ,lpep_pickup_datetime
  FROM
     green_taxi_trips
 group by lpep_pickup_datetime
 order by max_distance desc
 limit 1

 **Question 5. Three biggest pickup zones:**
select 
 taxi_zone_lookup.Zone,
 sum(total_amount) as total_revenue
  FROM
     green_taxi_trips
     inner join taxi_zone_lookup
     on green_taxi_trips.PULocationID = taxi_zone_lookup.LocationID
 where green_taxi_trips.lpep_pickup_datetime < '2019-11-01';
 group by Zone
HAVING 
    SUM(total_amount) > 13000
ORDER BY 
    total_revenue DESC
 limit 3
