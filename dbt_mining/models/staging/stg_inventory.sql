WITH raw_data AS (
    SELECT * FROM main.raw_inventory
)




SELECT
    TRIM(MINERAL_FILE_NUMBER) AS mineral_id,
    TRIM(MINFILE_NAME1) AS mine_name,
    YEAR AS inventory_year,
    TRIM(INVENTORY_CATEGORY_CODE) AS category_code,
    TRIM(INVENTORY_CATEGORY_DESCRIPTION) AS category_desc,
    TRIM(COMMODITY_CODE_1) AS commodity_code,
    TRIM(COMMODITY_DESCRIPTION1) AS commodity_desc,
    quantity AS tonnage,
    GRADE1 AS grade,
    DECIMAL_LATITUDE AS latitude,
    DECIMAL_LONGITUDE AS longitude,
    UTM_ZONE AS utm_zone,
    UTM_NORTHING AS utm_northing,
    UTM_EASTING AS utm_easting,
    TRIM(ORE_ZONE_DESCRIPTION) AS ore_zone_desc
FROM raw_data
