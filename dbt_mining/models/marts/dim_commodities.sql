SELECT DISTINCT
    commodity_code,
    commodity_desc,
    category_code,
    category_desc
FROM {{ ref('stg_inventory') }}
WHERE commodity_code IS NOT NULL
