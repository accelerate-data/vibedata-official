-- Existing convention: staging models retain source names.
select item_id, label from {{ source("inventory", "items") }}
