#!/usr/bin/env python
# coding: utf-8

import os
import argparse


import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    csv_name = params.csv_name

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

    trips = pd.read_csv(
        csv_name,
        parse_dates=True,
    )
    trips.to_sql(name=table_name, con=engine, if_exists="append", chunksize=10000)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument("--user", required=True, help="user name for postgres")
    parser.add_argument("--password", required=True, help="password for postgres")
    parser.add_argument("--host", required=True, help="host for postgres")
    parser.add_argument("--port", required=True, help="port for postgres")
    parser.add_argument("--db", required=True, help="database name for postgres")
    parser.add_argument(
        "--table_name",
        required=True,
        help="name of the table where we will write the results to",
    )
    parser.add_argument("--csv_name", required=True, help="path of the csv file")

    args = parser.parse_args()

    main(args)
