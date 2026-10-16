select item_id from {{ ref("stg_items") }} where item_id < 0
