# Week 3
# BigQuery Taxi Trip Data

This repository contains SQL queries for managing and analyzing NYC Yellow Taxi trip data using **Google BigQuery**.

## Table of Contents
- [Overview](#overview)
- [Queries](#queries)
  - [Create an External Table](#create-an-external-table)
  - [Query Sample Data](#query-sample-data)
  - [Create a Partitioned Table](#create-a-partitioned-table)
  - [Get Unique Vendor IDs (Non-Partitioned Table)](#get-unique-vendor-ids-non-partitioned-table)
  - [Get Unique Vendor IDs (Partitioned Table)](#get-unique-vendor-ids-partitioned-table)
  - [Check Table Partitions](#check-table-partitions)
- [License](#license)

## Overview

This project utilizes **Google BigQuery** to process NYC Yellow Taxi trip data stored in **Google Cloud Storage** in **Parquet format**. The queries include table creation, partitioning, data retrieval, and schema inspection.

---

## Queries

### Create an External Table
Creates an external table in BigQuery using a **Parquet file** stored in **Google Cloud Storage**.

```sql
CREATE OR REPLACE EXTERNAL TABLE `pivotal-surfer-449302.trips_all_data.yellow_tripdata`
OPTIONS (
  format ='parquet',
  uris =['gs://dtc_data_lake_pivotal-surfer-449302/raw/yellow_tripdata_2024-01.parquet']
);
```

### Query Sample Data
Retrieves the first **10 rows** from the external table.

```sql
SELECT * 
FROM `trips_all_data.yellow_tripdata`
LIMIT 10;
```

### Create a Partitioned Table
Creates a partitioned table based on the `tpep_pickup_datetime` column for optimized querying.

```sql
CREATE OR REPLACE TABLE pivotal-surfer-449302.trips_all_data.yellow_tripdata_partitoned
PARTITION BY DATE(tpep_pickup_datetime) AS 
SELECT * 
FROM `trips_all_data.yellow_tripdata`;
```

### Get Unique Vendor IDs (Non-Partitioned Table)
Retrieves distinct **VendorID** values for trips **between January 1 and January 30, 2024**.

```sql
SELECT DISTINCT(VendorID)
FROM trips_all_data.yellow_tripdata
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-01-01' AND '2024-01-30';
```

### Get Unique Vendor IDs (Partitioned Table)
Retrieves distinct **VendorID** values from the **partitioned table** for trips **between January 1 and January 30, 2024**.

```sql
SELECT DISTINCT(VendorID)
FROM `trips_all_data.yellow_tripdata_partitoned`
WHERE DATE(tpep_pickup_datetime) BETWEEN '2024-01-01' AND '2024-01-30';
```

### Check Table Partitions
Retrieves partition details for the **partitioned table**.

```sql
SELECT table_name, partition_id, total_rows
FROM `trips_all_data.INFORMATION_SCHEMA.PARTITIONS`
WHERE table_name = 'yellow_tripdata_partitoned'
ORDER BY partition_id DESC;
```

---

## License
This project is open-source and can be freely used or modified.
