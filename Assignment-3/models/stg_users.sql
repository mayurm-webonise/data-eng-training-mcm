-- Cleaned view of GreenWheel users: names uppercased, emails lowercased
-- for consistent downstream joins and reporting.

{{ config(materialized='view') }}

select
    user_id,
    upper(user_name) as user_name,
    lower(email) as email,
    created_at
from {{ source('greenwheel', 'raw_users') }}
