-- Cleaned view of GreenWheel's bike fleet. `model_type` is renamed to
-- `bike_model` since "model" is an overloaded/ambiguous term next to dbt models.

{{ config(materialized='view') }}

select
    bike_id,
    model_type as bike_model,
    rental_price,
    status
from {{ source('greenwheel', 'raw_bikes') }}
