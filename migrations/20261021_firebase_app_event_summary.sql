-- Keep app/event KPI summaries separate from country/version detail rows.
-- Requires the app identity and collection state migrations from 2026-10-20.
CREATE TABLE IF NOT EXISTS bt_adn_reports.firebase_app_event_daily
    LIKE bt_adn_reports.firebase_event_daily;
CREATE TABLE IF NOT EXISTS bt_adn_reports.firebase_app_collection_daily
    LIKE bt_adn_reports.firebase_collection_daily;
