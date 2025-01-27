import argparse
import os 
import pandas as pd
import numpy as np
import sqlalchemy as sqla

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    database = params.database
    table_name = params.table_name
    url = params.url
    lookup_url = params.lookup_url
    csv_path = './csv_data'
    csv_file = 'green_tripdata_2019-10.csv'
    lookup_csv_file = 'taxi_zone_lookup.csv'
     
   
    # # csv_file_path = os.path.join(csv_path, csv_file)
    # # lookup_csv_file_path = os.path.join(csv_path, lookup_csv_file)

    # print(csv_file_path)
    # Download the main CSV file
    os.system(f'wget {url} -O {csv_file}')
    print(f'Downloaded {csv_file} from {url}')

    # Download the lookup CSV file
    os.system(f'wget {lookup_url} -O {lookup_csv_file}')
    print(f'Downloaded {lookup_csv_file} from {lookup_url}')
    
    engine = sqla.create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}') 
    
    lookup_df = pd.read_csv(lookup_csv_file)
    lookup_df.to_sql('taxi_zone_lookup', engine, if_exists='replace', index=False)
     
    df_itr = pd.read_csv(csv_file, compression="gzip", chunksize=100000)
    df = next(df_itr)
    # Convert datetime columns
    df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
    df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])

    # Create the table and insert the first chunk
    df.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

    # Process and insert remaining chunks
    for i, df in enumerate(df_itr):
        df['lpep_pickup_datetime'] = pd.to_datetime(df['lpep_pickup_datetime'])
        df['lpep_dropoff_datetime'] = pd.to_datetime(df['lpep_dropoff_datetime'])
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f"Chunk {i+1} inserted successfully.")

    print("Data ingestion completed successfully.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest data from CSV to PostgreSQL')  
    parser.add_argument('--user', type=str, help='PostgreSQL username')
    parser.add_argument('--password', type=str, help='PostgreSQL password')
    parser.add_argument('--host', type=str, help='PostgreSQL host')
    parser.add_argument('--port', type=str, help='PostgreSQL port')
    parser.add_argument('--database', type=str, help='PostgreSQL database')
    parser.add_argument('--table_name', type=str, help='PostgreSQL table')
    parser.add_argument('--url', type=str, help='URL to download CSV file')
    parser.add_argument('--lookup_url', type=str, help='URL to download lookup CSV file')   

    args = parser.parse_args()
    main(args)