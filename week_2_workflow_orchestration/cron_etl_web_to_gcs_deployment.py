from prefect.orion.schemas.schedules import CronSchedule
from prefect.deployments import Deployment

from etl_web_to_gcs import etl_parent_flow

Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="ETL to GCS deployment (Jan 2020 green)",
    schedule=(CronSchedule(cron="0 5 1 * *", timezone="UTC")),
    parameters={"year": 2020, "months": [1], "color": "green"},
    apply=True,
)

Deployment.build_from_flow(
    flow=etl_parent_flow,
    name="ETL to GCS deployment (Feb. Mar 2019 yellow)",
    parameters={"year": 2019, "months": [2, 3], "color": "yellow"},
    apply=True,
)
