SELECT DISTINCT
    mineral_id,
    mine_name,
    latitude,
    longitude,
    utm_zone,
    utm_northing,
    utm_easting
FROM {{ ref('stg_inventory') }}
WHERE mineral_id IS NOT NULL
