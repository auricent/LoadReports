-- Apply before deploying the loader and daily report that use completion state.
CREATE TABLE IF NOT EXISTS bt_adn_reports.firebase_collection_daily (
    day DATE NOT NULL,
    stream_id VARCHAR(64) NOT NULL,
    app_id VARCHAR(255) NOT NULL,
    source_sha256 CHAR(64) NOT NULL,
    imported_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (day, stream_id),
    INDEX day_app_idx (day, app_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
