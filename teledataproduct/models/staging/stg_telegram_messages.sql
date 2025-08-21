-- models/staging/stg_telegram_messages.sql

with raw_messages as (

    select *
    from raw.telegram_messages

),

renamed as (

    select
        id::bigint                                         as message_id,
        trim(channel)                                      as channel_name,
        cast(date_val as timestamp)                        as message_timestamp,
        -- nullif(sender_id, '')::bigint                      as sender_id,
        case 
            when sender_id::text ~ '^[0-9]+$' then sender_id::bigint
            else null
        end as sender_id,

        trim(message)                                      as message_text,
        coalesce(has_media::boolean, false)                as has_media,
        nullif(media_path, '')                             as media_path,
        length(trim(message))                              as message_length
    from raw_messages

)

select *
from renamed



-- select
--     id,
--     channel,
--     date_val::timestamp as date_val,
--     sender_id::bigint as sender_id,
--     message,
--     has_media::boolean as has_media,
--     media_path,
--     length(message) as message_length  -- derived column
-- from raw_messages
