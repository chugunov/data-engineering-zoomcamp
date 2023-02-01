import os
from datetime import timedelta
from pathlib import Path


import pandas as pd
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_gcp.cloud_storage import GcsBucket


@task(
    log_prints=True,
    tags=["extract"],
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
)
def extract_dataset(month: int, year: int, color: str) -> pd.DataFrame:
    url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{color}_tripdata_{year}-{month:02}.csv.gz"
    print(f"Load dataset from {url} to pandas dataframe")
    df = pd.read_csv(url, parse_dates=True)
    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task(log_prints=True)
def write_local(df: pd.DataFrame, month: int, year: int, color: str) -> Path:
    path = Path(f"data/{color}/{color}_tripdata_{year}-{month:02}.parquet")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path, compression="gzip")
    return path


@task(log_prints=True, retries=3)
def write_gcs(path: Path) -> None:
    gcs_block = GcsBucket.load("zoom-gcs")
    gcs_block.upload_from_path(from_path=path, to_path=path, timeout=300)


@flow
def etl_web_to_gcs(month, year, color):
    df = extract_dataset(month, year, color)
    path = write_local(df, month, year, color)
    write_gcs(path)
    return


@flow
def etl_parent_flow(months: list[int], year: int, color: str):
    for month in months:
        etl_web_to_gcs(month, year, color)


if __name__ == "__main__":
    etl_parent_flow([2, 3], 2019, "yellow")
