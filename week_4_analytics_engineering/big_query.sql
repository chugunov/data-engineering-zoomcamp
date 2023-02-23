CREATE OR REPLACE TABLE `taxi-rides-ny.nytaxi.fhv_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = [
    'gs://dtc_data_lake_dtc-de-course-376117/data/fhv/fhv_tripdata_2019-*.parquet',
    'gs://dtc_data_lake_dtc-de-course-376117/data/green/green_tripdata_2019-*.parquet',
    'gs://dtc_data_lake_dtc-de-course-376117/data/green/green_tripdata_2020-*.parquet',
    'gs://dtc_data_lake_dtc-de-course-376117/data/yellow/yellow_tripdata_2019-*.parquet',
    'gs://dtc_data_lake_dtc-de-course-376117/data/yellow/yellow_tripdata_2020-*.parquet',
  ]
);