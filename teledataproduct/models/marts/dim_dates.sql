-- models/marts/dim_dates.sql

with dates as (
    select distinct date(message_timestamp) as message_date
    from {{ ref('stg_telegram_messages') }}
)

select
    row_number() over() as date_id,
    message_date,
    extract(year from message_date) as year,
    extract(month from message_date) as month,
    extract(day from message_date) as day,
    to_char(message_date, 'Day') as day_name
from dates
