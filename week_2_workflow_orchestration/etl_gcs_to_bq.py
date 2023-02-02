from pathlib import Path
from datetime import timedelta
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp import GcpCredentials
from prefect.tasks import task_input_hash


@task(
    retries=3,
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def extract_from_gcs(month: int, year: int, color: str) -> Path:
    """Download trip data from GCS"""
    gcs_path = f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet"
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.get_directory(from_path=gcs_path, local_path=f"../data/")
    return Path(f"../data/{gcs_path}")


@task()
def load_to_dataframe(path: Path) -> pd.DataFrame:
    """Load parquet file to DataFrame"""
    df = pd.read_parquet(path)
    return df


@task()
def write_bq(df: pd.DataFrame) -> None:
    """Write DataFrame to BiqQuery"""
    gcp_credentials_block = GcpCredentials.load("zoom-gcp-creds")

    df.to_gbq(
        destination_table="dezoomcamp.rides",
        project_id="dtc-de-course-376117",
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )


@flow(log_prints=True)
def etl_gcs_to_bq(month: int, year: int, color: str):
    """Main ETL flow to load data into Big Query"""
    path = extract_from_gcs(month, year, color)
    df = load_to_dataframe(path)
    print(f"rows: {len(df)}")
    write_bq(df)


@flow()
def etl_parent_flow(months: list[int], year: int, color: str):
    for month in months:
        etl_gcs_to_bq(month, year, color)


if __name__ == "__main__":
    etl_parent_flow([2, 3], 2019, "yellow")
