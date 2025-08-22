-- returns rows that violate the rule -> test fails if any
select *
from {{ ref('stg_image_detections') }}
where (confidence_score < 0 or confidence_score > 1)
