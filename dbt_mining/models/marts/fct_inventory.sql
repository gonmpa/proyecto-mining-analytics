SELECT
    mineral_id,
    commodity_code,
    inventory_year,
    tonnage,
    grade,
    ore_zone_desc
FROM {{ ref('stg_inventory') }}
WHERE inventory_year IS NOT NULL
