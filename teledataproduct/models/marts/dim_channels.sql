-- models/marts/dim_channels.sql

with channels as (
    select distinct channel_name
    from {{ ref('stg_telegram_messages') }}
)

select
    row_number() over() as channel_id,
    channel_name
from channels
