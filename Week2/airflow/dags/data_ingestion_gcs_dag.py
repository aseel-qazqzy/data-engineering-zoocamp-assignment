import os 
import logging
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator

import pyarrow.csv as pv
import pyarrow.parquet as pq

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET_NAME = os.environ.get("GCP_GCS_BUCKET")

if not BUCKET_NAME:
    raise ValueError("GCP_GCS_BUCKET environment variable is not set!")

dataset_file = "yellow_tripdata_2024-01.parquet"
dataset_url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{dataset_file}"
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow")
parquet_file = "yellow_tripdata_2024-01.parquet"
BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", "trips_all_data")

def format_to_parquet(src_file):
    if not os.path.exists(src_file):
        logging.error(f"File not found: {src_file}")
        raise FileNotFoundError(f"File not found: {src_file}")

    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format")
        return
    
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace(".csv", ".parquet"))

def upload_to_gcs(bucket, object_name, local_file):
    """Uploads a file to Google Cloud Storage (GCS)."""
    if not os.path.exists(local_file):
        logging.error(f"Local file not found: {local_file}")
        raise FileNotFoundError(f"Local file not found: {local_file}")
    
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5MB 

    client = storage.Client()
    bucket = client.bucket(bucket)
    blob = bucket.blob(object_name)

    if not os.path.exists(local_file):
        logging.error(f"Local file not found: {local_file}")
        raise FileNotFoundError(f"Local file not found: {local_file}")

    blob.upload_from_filename(local_file)

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1
}

# Define the DAG
with DAG(
    dag_id="data_ingestion_gcs_dag",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=["dtc-de"], 
) as dag: 
    
    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"sleep 10 && curl -sSL {dataset_url} -o {path_to_local_home}/{dataset_file}"
    )
    

    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET_NAME,
            "object_name": f"raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}"
        }
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
        task_id="bigquery_external_table_task",
        table_resource={
            "tableReference": {
                "projectId": PROJECT_ID,
                "datasetId": BIGQUERY_DATASET,
                "tableId": "external_table",
            },
            "externalDataConfiguration": {
                "sourceFormat": "PARQUET",
                "sourceUris": [f"gs://{BUCKET_NAME}/raw/{parquet_file}"],
            },
        },
    )

    download_dataset_task >> local_to_gcs_task >> bigquery_external_table_task
