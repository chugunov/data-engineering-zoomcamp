from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment

from etl_gcs_to_bq import etl_parent_flow

cron_deployment = Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="GCS to BQ deployment",
    schedule=(CronSchedule(cron="0 5 1 * *", timezone="UTC")),
    parameters={
        "dataset_file": "green_trips",
        "url": "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-01.csv.gz",
    },
)
cron_deployment.apply()
