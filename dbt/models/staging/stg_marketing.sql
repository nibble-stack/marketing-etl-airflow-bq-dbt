-- models/staging/stg_marketing.sql

WITH source AS (
    SELECT
        timestamp,
        temperature,
        precipitation,
        impressions,
        clicks,
        conversions,
        spend,
        extracted_at
    FROM `{{ env_var('GCP_PROJECT_ID') }}.{{ env_var('BIGQUERY_DATASET') }}.raw_marketing_data`
)

SELECT
    timestamp,
    DATE(timestamp) AS date,
    temperature,
    precipitation,
    impressions,
    clicks,
    conversions,
    spend,
    extracted_at
FROM source
