-- tests/media_path_not_null.sql
select *
from {{ ref('stg_telegram_messages') }}
where has_media = true
and media_path is null
