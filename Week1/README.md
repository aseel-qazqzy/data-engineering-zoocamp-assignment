# Week 1
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-10.csv.gz"

lookup_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

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
    --lookup_url= ${lookup_url} 
