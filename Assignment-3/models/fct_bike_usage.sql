-- One row per bike: how many trips it's taken, total revenue it's generated,
-- and total minutes ridden. Built as a table since this feeds reporting
-- directly and is worth materializing rather than recomputing on every query.
--
-- Note: raw_trips contains at least one dirty record (trip_id 5015 has a
-- negative trip_duration_seconds). It is intentionally NOT filtered out here
-- since the assignment doesn't ask for it -- but it will skew
-- total_minutes_ridden slightly downward for bike 101. Worth a follow-up
-- data-quality test if this were a real production model.

{{ config(materialized='table') }}

with trips as (

    select
        trip_id,
        user_id,
        bike_id,
        trip_duration_seconds,
        trip_cost,
        trip_at
    from {{ source('greenwheel', 'raw_trips') }}

),

bikes as (

    select * from {{ ref('stg_bikes') }}

),

bike_usage as (

    select
        bikes.bike_id,
        bikes.bike_model,
        bikes.status,
        count(trips.trip_id) as total_trips,
        coalesce(sum(trips.trip_cost), 0) as total_cost,
        coalesce(sum(trips.trip_duration_seconds), 0) / 60.0 as total_minutes_ridden
    from bikes
    left join trips on trips.bike_id = bikes.bike_id
    group by
        bikes.bike_id,
        bikes.bike_model,
        bikes.status

)

select * from bike_usage
