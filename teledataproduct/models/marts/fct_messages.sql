-- models/marts/fct_messages.sql

with messages as (
    select
        m.message_id,
        m.sender_id,
        m.message_text,
        m.has_media,
        m.message_length,
        d.date_id,
        c.channel_id
    from {{ ref('stg_telegram_messages') }} m
    join {{ ref('dim_dates') }} d
        on date(m.message_timestamp) = d.message_date
    join {{ ref('dim_channels') }} c
        on m.channel_name = c.channel_name
)

select *
from messages
