# GreenWheel dbt Foundations Assignment

A minimal dbt project for GreenWheel, an electric bike-share startup, built to
satisfy the "GreenWheel dbt Foundation Assignment" (Quick-Start Analytics
Engineering Workshop).

## Project layout

```
greenwheel_dbt/
├── dbt_project.yml
├── seeds/
│   ├── raw_users.csv
│   ├── raw_bikes.csv
│   └── raw_trips.csv
├── models/
│   ├── stg_users.sql        -- view: users, name upper-cased, email lower-cased
│   ├── stg_bikes.sql        -- view: bikes, model_type renamed to bike_model
│   ├── fct_bike_usage.sql   -- table: trips + bikes joined, aggregated per bike
│   └── schema.yml           -- sources, docs, and generic tests
└── README.md
```

## 1. Set up your profile

This project expects a profile named `greenwheel` in `~/.dbt/profiles.yml`.
Point it at whatever warehouse you're using. Two examples:

**DuckDB (fastest way to try this locally, no server needed):**
```yaml
greenwheel:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: greenwheel.duckdb
      threads: 4
```
(Requires the `dbt-duckdb` adapter: `pip install dbt-duckdb`.)

**Snowflake:**
```yaml
greenwheel:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your_account>
      user: <your_user>
      authenticator: externalbrowser   # or password / key-pair, per your org's setup
      role: <your_role>
      database: <your_database>
      warehouse: <your_warehouse>
      schema: greenwheel_dev
      threads: 4
```

Never commit `profiles.yml` or credentials to version control -- it lives
outside this project folder by default.

## 2. Install dependencies (if any) and check the connection

```bash
dbt deps        # no-op here, no packages declared, but harmless to run
dbt debug        # confirms dbt can reach your warehouse
```

## 3. Load the seeds

```bash
dbt seed
```
This creates `raw_users`, `raw_bikes`, and `raw_trips` tables in your target
schema from the CSVs in `seeds/`.

## 4. Build the models

```bash
dbt run
```
Builds `stg_users` and `stg_bikes` as views, and `fct_bike_usage` as a table.

## 5. Test the data

```bash
dbt test
```
Runs `unique` + `not_null` checks on `user_id` (raw_users/stg_users),
`bike_id` (raw_bikes/stg_bikes/fct_bike_usage), and `trip_id` (raw_trips).

## 6. Generate and browse docs

```bash
dbt docs generate && dbt docs serve
```

## Known data quality note

`raw_trips.csv` row `trip_id = 5015` has `trip_duration_seconds = -500`
(bike 101). It's left in `fct_bike_usage` unfiltered since the assignment
doesn't call for cleaning it, but it does pull `total_minutes_ridden` down
slightly for bike 101. Worth a `dbt_utils.accepted_range` test on
`trip_duration_seconds >= 0` if this were a real production pipeline.
