# Week 1
**Question 1. Understanding docker first run:**
**- Run docker in intractive mode:**
docker run -it --entrypoint=bash python:3.12.8
```

### Get the PIP Version:
```bash
pip --version
```

---

## **Question 2: Docker Networking and Docker-Compose**

### Build the Image:
```bash
docker build -t ingest_green_tripdata:v001 .
```

### Run the Image:
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"
lookup_url="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

docker run -it \
    --network=week1_default \
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
```

### Use PGCLI to Connect to the Database:
```bash
pgcli -h localhost -p 5434 -u postgres -d ny_taxi
```

---

## **Question 3: Trip Segmentation Count**

**During the period of October 1st, 2019 (inclusive) and November 1st, 2019 (exclusive), how many trips occurred:**
- **Up to 1 mile**
- **Between 1 (exclusive) and 3 miles (inclusive)**
- **Between 3 (exclusive) and 7 miles (inclusive)**
- **Between 7 (exclusive) and 10 miles (inclusive)**
- **Over 10 miles**

### Query:
```sql
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
```

---

## **Question 4: Maximum Trip Distance**

### Query:
```sql
SELECT 
    MAX(trip_distance) AS max_distance,
    lpep_pickup_datetime
FROM
    green_taxi_trips
GROUP BY 
    lpep_pickup_datetime
ORDER BY 
    max_distance DESC
LIMIT 1;
```

---

## **Question 5: Three Biggest Pickup Zones**

### Query:
```sql
SELECT 
    taxi_zone_lookup.Zone,
    SUM(total_amount) AS total_revenue
FROM
    green_taxi_trips
    INNER JOIN taxi_zone_lookup
    ON green_taxi_trips.PULocationID = taxi_zone_lookup.LocationID
WHERE 
    green_taxi_trips.lpep_pickup_datetime < '2019-11-01'
GROUP BY 
    Zone
HAVING 
    SUM(total_amount) > 13000
ORDER BY 
    total_revenue DESC
LIMIT 3;
```

---

## **Question 6: Largest Tip**

### Query:
```sql
SELECT 
    dropoff_zone.Zone AS dropoff_zone,
    MAX(green_taxi_trips.tip_amount) AS largest_tip
FROM 
    green_taxi_trips
INNER JOIN 
    taxi_zone_lookup AS pickup_zone
ON 
    green_taxi_trips.PULocationID = pickup_zone.LocationID
INNER JOIN 
    taxi_zone_lookup AS dropoff_zone
ON 
    green_taxi_trips.DOLocationID = dropoff_zone.LocationID
WHERE 
    pickup_zone.Zone = 'East Harlem North' 
    AND green_taxi_trips.lpep_pickup_datetime >= '2019-10-01'
    AND green_taxi_trips.lpep_pickup_datetime < '2019-11-01'
GROUP BY 
    dropoff_zone.Zone
ORDER BY 
    largest_tip DESC
LIMIT 1;
```
