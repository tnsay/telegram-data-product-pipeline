-- models/facts/fct_image_detections.sql

with d as (
    select
        detection_id,
        message_id,
        detected_object_class,
        confidence_score,
        media_path,
        yolo_model,
        run_ts
    from {{ ref('stg_image_detections') }}
),

m as (
    select
        message_id,
        channel_name,
        message_timestamp,
        has_media
    from {{ ref('stg_telegram_messages') }}
)

select
    d.detection_id,
    d.message_id,
    m.channel_name,
    m.message_timestamp,
    m.has_media,
    d.detected_object_class,
    d.confidence_score,
    d.media_path,
    d.yolo_model,
    d.run_ts
from d
left join m using (message_id)
