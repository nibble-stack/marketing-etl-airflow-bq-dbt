-- models/marts/fct_marketing_performance.sql

WITH base AS (
    SELECT *
    FROM {{ ref('stg_marketing') }}
)

SELECT
    date,
    SUM(impressions) AS impressions,
    SUM(clicks) AS clicks,
    SUM(conversions) AS conversions,
    SUM(spend) AS spend,

    SAFE_DIVIDE(SUM(clicks), SUM(impressions)) AS ctr,
    SAFE_DIVIDE(SUM(spend), SUM(clicks)) AS cpc,
    SAFE_DIVIDE(SUM(spend), SUM(conversions)) AS cpa,
    SAFE_DIVIDE(SUM(conversions), SUM(clicks)) AS conversion_rate,
    SAFE_DIVIDE(SUM(conversions) * 50, SUM(spend)) AS roas  -- assume $50 per conversion
FROM base
GROUP BY date
ORDER BY date
