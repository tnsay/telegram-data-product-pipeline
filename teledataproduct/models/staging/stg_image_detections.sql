-- models/staging/stg_image_detections.sql

with raw as (
    select
        detection_id::bigint                              as detection_id,
        message_id::bigint                                as message_id,
        lower(trim(detected_object_class))                as detected_object_class,
        round(confidence_score::numeric, 3)               as confidence_score,
        media_path,
        yolo_model,
        run_ts::timestamp                                 as run_ts
    from raw.image_detections
)

select *
from raw
