-- Apply once before deploying the updated loader and daily report.
ALTER TABLE bt_adn_reports.firebase_event_daily
    ADD COLUMN stream_id VARCHAR(64) NOT NULL DEFAULT '' COMMENT 'GA4 data stream ID',
    ADD COLUMN app_id VARCHAR(255) NOT NULL DEFAULT '' COMMENT 'Apple bundle ID or Android package name',
    ADD INDEX day_app_event_idx (`day`, `app_id`, `event_name`);

-- Existing rows cannot be attributed to an app. Recollect the required dates
-- with the updated report-data-job, then reload firebase_event_daily.csv.
