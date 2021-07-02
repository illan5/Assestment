
-- FIELDS: timestamp_utc, campaign_name, event_type, revenue
SELECT * FROM raw_campaign_events;

-- FIELDS: campaign_name, visits, impressions, last_impressed_at_pst, conversions, last_converted_at_pst, total_revenue
-- NOTE: visits, impressions and conversions are the sum of each of their events (event_type)
CREATE TABLE campaign_events_pst AS
    SELECT campaign_name,
        SUM(CASE event_type WHEN 'visit_created' THEN 1 ELSE 0) AS visits,
        SUM(CASE event_type WHEN 'campaign_impressed' THEN 1 ELSE 0) AS impressions,
        MAX(CASE event_type WHEN 'campaign_impressed' THEN timestamp_utc ELSE 0) AS last_impressed_at_pst,
        SUM(CASE event_type WHEN 'campaign_converted' THEN 1 ELSE 0) AS conversions,
        MAX(CASE event_type WHEN 'campaign_converted' THEN timestamp_utc ELSE 0) AS last_converted_at_pst,
        SUM(IF(revenue IS NULL, 0, revenue)) AS total_revenue
    FROM raw_campaign_events
    GROUP BY campaign_name;

