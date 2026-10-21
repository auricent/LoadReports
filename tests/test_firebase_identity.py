import csv
from datetime import date

from src.processors.firebase import FirebaseProcessor


def test_firebase_loader_preserves_distinct_apps(tmp_path):
    path = tmp_path / 'firebase_event_daily.csv'
    columns = [
        'day', 'event_name', 'platform', 'operating_system', 'app_version',
        'country', 'event_count', 'total_users', 'active_users', 'stream_id', 'app_id',
    ]
    with path.open('w', newline='') as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        for stream, app in [('101', 'com.bittorrent.client-macOS'), ('202', 'com.utorrent.client-macOS')]:
            writer.writerow(['2026-10-18', 'first_open', 'iOS', 'Macintosh', '1.3.0', 'US', '10', '9', '8', stream, app])

    rows = [row.to_dict() for row in FirebaseProcessor().process_data(str(path))]
    assert rows[0]['app_id'] == 'com.bittorrent.client-macOS'
    assert rows[1]['app_id'] == 'com.utorrent.client-macOS'
    assert rows[1]['stream_id'] == '202'
    assert rows[1]['day'] == date(2026, 10, 18)
    assert rows[1]['event_count'] == 10


def test_legacy_firebase_csv_keeps_app_unknown(tmp_path):
    path = tmp_path / 'legacy.csv'
    path.write_text('day,event_name,platform,event_count,total_users,active_users\n2026-06-13,first_open,iOS,3,3,3\n')
    row = FirebaseProcessor().process_data(str(path))[0].to_dict()
    assert row['app_id'] == ''
    assert row['stream_id'] == ''
    assert row['event_count'] == 3
