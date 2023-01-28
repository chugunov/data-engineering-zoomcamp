## Week 1 Homework

In this homework we'll prepare the environment
and practice with Docker and SQL

## Question 1. Knowing docker tags

Run the command to get information on Docker

`docker --help`

Now run the command to get help on the "docker build" command

Which tag has the following text? - _Write the image ID to the file_

- `--iidfile string`

### Docker command output

```bash
$ docker build --help

Usage:  docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile

Options:
      --add-host list           Add a custom host-to-IP mapping (host:ip)
      --build-arg list          Set build-time variables
      --cache-from strings      Images to consider as cache sources
      --disable-content-trust   Skip image verification (default true)
  -f, --file string             Name of the Dockerfile (Default is 'PATH/Dockerfile')
      --iidfile string          Write the image ID to the file
      --isolation string        Container isolation technology
      --label list              Set metadata for an image
      --network string          Set the networking mode for the RUN instructions during build (default "default")
      --no-cache                Do not use cache when building the image
  -o, --output stringArray      Output destination (format: type=local,dest=path)
      --platform string         Set platform if server is multi-platform capable
      --progress string         Set type of progress output (auto, plain, tty). Use plain to show container output (default "auto")
      --pull                    Always attempt to pull a newer version of the image
  -q, --quiet                   Suppress the build output and print image ID on success
      --secret stringArray      Secret file to expose to the build (only if BuildKit enabled): id=mysecret,src=/local/secret
      --ssh stringArray         SSH agent socket or keys to expose to the build (only if BuildKit enabled) (format: default|<id>[=<socket>|<key>[,<key>]])
  -t, --tag list                Name and optionally a tag in the 'name:tag' format
      --target string           Set the target build stage to build.
```

## Question 2. Understanding docker first run

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use pip list).
How many python packages/modules are installed?

- 3

### Docker command

```bash
$ docker run -it python:3.9 pip list
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4
WARNING: You are using pip version 22.0.4; however, version 22.3.1 is available.
You should consider upgrading via the '/usr/local/bin/python -m pip install --upgrade pip' command.
```

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from January 2019:

`wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz`

You will also need the dataset with zones:

`wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv`

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

_My notes:_ I updated `ingest_data.py` script. Because of slow internet speed I had to remove `wget` downloading feature and just added `csv` arg to pass csv path directly.

```bash
$ docker-compose up -d
$ wget -P ./datasets https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-01.csv.gz
$ wget -P ./datasets https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install pandas sqlalchemy psycopg2
$ python ingest_data.py \                                                               Py data-engineering-zoomcamp
    --user=root \
    --password=root \
    --host=0.0.0.0 \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --csv_name=./datasets/taxi+_zone_lookup.csv
$ python ingest_data.py \                                                               Py data-engineering-zoomcamp
    --user=root \
    --password=root \
    --host=0.0.0.0 \
    --port=5432 \
    --db=ny_taxi \
    --table_name=green_taxi_trips \
    --csv_name=./datasets/green_tripdata_2019-01.csv.gz
```

## Question 3. Count records

How many taxi trips were totally made on January 15?

Tip: started and finished on 2019-01-15.

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 20530

### SQL query

```sql
select count(1) from green_taxi_trips
where lpep_pickup_datetime >= '2019-01-15 00:00:00' and lpep_dropoff_datetime < '2019-01-16 00:00:00'
```

## Question 4. Largest trip for each day

Which was the day with the largest trip distance
Use the pick up time for your calculations.

- 2019-01-15

### SQL query

```sql
select date(lpep_pickup_datetime) from green_taxi_trips
order by trip_distance desc
limit 1
```

## Question 5. The number of passengers

In 2019-01-01 how many trips had 2 and 3 passengers?

- 2: 1282 ; 3: 254

### SQL query

```sql
select passenger_count, count(1) from green_taxi_trips
where lpep_pickup_datetime >= '2019-01-01' and lpep_pickup_datetime < '2019-01-02' and passenger_count in (2, 3)
group by passenger_count
```

## Question 6. Largest tip

For the passengers picked up in the Astoria Zone which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Long Island City/Queens Plaza

### SQL query

```sql
SELECT tip_amount, a."ZZone" as "PUZone", "Zone" as "DOZone"
FROM (SELECT tip_amount, "Zone" as "ZZone", "DOLocationID", "PULocationID"
FROM green_taxi_trips
INNER JOIN zones ON "PULocationID"="LocationID"
where "Zone" = 'Astoria'
order by tip_amount desc) a
INNER JOIN zones ON "DOLocationID"="LocationID"
limit 1
```

## Submitting the solutions

- Form for submitting: [form](https://forms.gle/EjphSkR1b3nsdojv7)
- You can submit your homework multiple times. In this case, only the last submission will be used.

Deadline: 30 January (Monday), 22:00 CET

## Solution

We will publish the solution here
