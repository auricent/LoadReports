import hashlib
import io
import json
import sqlite3
from datetime import date

import pytest
from botocore.exceptions import ClientError

from src.models.firebase import FirebaseReport
from src.processors.firebase import FirebaseProcessor, FirebaseAppEventProcessor
from src.processors.processor import DataProcessor
from src.util.database import DatabaseClient


DAY = '2026-10-18'
APP = 'com.utorrent.client-macOS'
HEADER = 'day,event_name,platform,operating_system,app_version,country,event_count,total_users,active_users,stream_id,app_id\n'


class SQLiteCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, sql, params):
        return self.cursor.execute(sql.replace('%s', '?'), params)

    def executemany(self, sql, rows):
        values = [tuple(str(value) if isinstance(value, date) else value for value in row) for row in rows]
        return self.cursor.executemany(sql.replace('%s', '?'), values)

    def close(self):
        self.cursor.close()


class SQLiteConnection:
    def __init__(self):
        self.raw = sqlite3.connect(':memory:')
        self.raw.executescript('''
            CREATE TABLE firebase_event_daily (
                day TEXT, event_name TEXT, platform TEXT, operating_system TEXT,
                app_version TEXT, country TEXT, event_count INTEGER,
                total_users INTEGER, active_users INTEGER, stream_id TEXT, app_id TEXT
            );
            CREATE TABLE firebase_collection_daily (
                day TEXT, stream_id TEXT, app_id TEXT,
                source_sha256 TEXT CHECK(length(source_sha256) = 64),
                PRIMARY KEY(day, stream_id)
            );
        ''')
        for old, new in [('firebase_event_daily', 'firebase_app_event_daily'),
                         ('firebase_collection_daily', 'firebase_app_collection_daily')]:
            schema = self.raw.execute('SELECT sql FROM sqlite_master WHERE name = ?', (old,)).fetchone()[0]
            self.raw.execute(schema.replace(old, new))

    def is_connected(self):
        return True

    def cursor(self):
        return SQLiteCursor(self.raw.cursor())

    def commit(self):
        self.raw.commit()

    def rollback(self):
        self.raw.rollback()


@pytest.fixture
def database():
    db = DatabaseClient(None)
    db.connection = SQLiteConnection()
    yield db
    db.connection.raw.close()


def write_pair(tmp_path, body=HEADER):
    csv_path = tmp_path / 'firebase_event_daily.csv'
    csv_path.write_bytes(body.encode())
    manifest_path = tmp_path / 'firebase_event_daily.complete.json'
    manifest_path.write_text(json.dumps({
        'schema_version': 1,
        'day': DAY,
        'source_sha256': hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        'apps': {'202': APP},
    }))
    return csv_path, manifest_path


def sample_report():
    return FirebaseReport(
        day=date.fromisoformat(DAY), event_name='first_open', platform='iOS',
        operating_system='Macintosh', app_version='1.3.0', country='US',
        event_count=10, total_users=10, active_users=10, stream_id='202', app_id=APP,
    )


def test_complete_empty_csv_replaces_stale_events_and_records_zero_day(tmp_path, database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    csv_path, manifest_path = write_pair(tmp_path)
    processor = FirebaseProcessor()
    reports = processor.process_data(str(csv_path))
    completion = processor.process_completion_manifest(str(csv_path), str(manifest_path), DAY, reports)
    database.replace_firebase_day(DAY, reports, **completion)
    assert database.connection.raw.execute('SELECT COUNT(*) FROM firebase_event_daily').fetchone()[0] == 0
    row = database.connection.raw.execute('SELECT day, app_id, source_sha256 FROM firebase_collection_daily').fetchone()
    assert row == (DAY, APP, hashlib.sha256(csv_path.read_bytes()).hexdigest())


def test_mismatched_manifest_is_rejected_before_database_replacement(tmp_path):
    csv_path, manifest_path = write_pair(tmp_path)
    csv_path.write_bytes(csv_path.read_bytes() + b'\n')
    with pytest.raises(ValueError, match='does not match'):
        FirebaseProcessor().process_completion_manifest(str(csv_path), str(manifest_path), DAY, [])


def test_manifest_for_another_day_is_rejected(tmp_path):
    csv_path, manifest_path = write_pair(tmp_path)
    with pytest.raises(ValueError, match='version or date'):
        FirebaseProcessor().process_completion_manifest(str(csv_path), str(manifest_path), '2026-10-17', [])


def test_manifest_must_include_the_event_app_identity(tmp_path):
    csv_path, manifest_path = write_pair(tmp_path)
    report = sample_report()
    report.app_id = 'com.bittorrent.client-macOS'
    with pytest.raises(ValueError, match='absent'):
        FirebaseProcessor().process_completion_manifest(str(csv_path), str(manifest_path), DAY, [report])


def test_database_failure_rolls_back_events_and_completion(database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    with pytest.raises(sqlite3.IntegrityError):
        database.replace_firebase_day(DAY, [], {'202': APP}, 'invalid-hash')
    assert database.connection.raw.execute('SELECT event_count FROM firebase_event_daily').fetchone()[0] == 10
    assert database.connection.raw.execute('SELECT source_sha256 FROM firebase_collection_daily').fetchone()[0] == 'a' * 64


def test_import_without_manifest_clears_old_completion_state(database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    database.replace_firebase_day(DAY, [sample_report()], {}, '')
    assert database.connection.raw.execute('SELECT COUNT(*) FROM firebase_collection_daily').fetchone()[0] == 0


def test_invalid_empty_csv_does_not_count_as_success(tmp_path):
    path = tmp_path / 'empty.csv'
    path.write_bytes(b'')
    with pytest.raises(ValueError, match='required columns'):
        FirebaseProcessor().process_data(str(path))


def test_csv_with_wrong_date_is_rejected_before_delete(database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    report = sample_report()
    report.day = date(2026, 10, 17)
    with pytest.raises(ValueError, match='different report date'):
        database.replace_firebase_day(DAY, [report], {}, '')
    assert database.connection.raw.execute('SELECT event_count FROM firebase_event_daily').fetchone()[0] == 10


def run_s3_import(monkeypatch, database, manifest_error=None, corrupt_hash=False, summary=False, quality_verified=True):
    csv_body = HEADER.encode()
    filename = 'firebase_app_event_daily' if summary else 'firebase_event_daily'
    manifest_body = json.dumps({
        'schema_version': 1, 'day': DAY,
        'source_sha256': 'bad' if corrupt_hash else hashlib.sha256(csv_body).hexdigest(),
        'apps': {'202': APP},
        'aggregation': 'app_event' if summary else '',
        'quality_verified': quality_verified,
    }).encode()
    downloads = []

    class MemoryS3:
        def list_files(self, prefix):
            return [prefix + '/' + filename + '.complete.json', prefix + '/' + filename + '.csv']

        def download_file(self, key, path):
            downloads.append(key)
            if key.endswith('.json') and manifest_error:
                raise ClientError({'Error': {'Code': manifest_error}}, 'GetObject')

    original_open = open

    def artifact_open(path, mode='r', *args, **kwargs):
        if str(path) == '/tmp/' + filename + '.csv':
            return io.BytesIO(csv_body) if 'b' in mode else io.StringIO(csv_body.decode())
        if str(path) == '/tmp/' + filename + '.csv.complete.json':
            return io.StringIO(manifest_body.decode())
        return original_open(path, mode, *args, **kwargs)

    monkeypatch.setattr('builtins.open', artifact_open)
    processor = DataProcessor(MemoryS3(), database)
    processor.process_s3_files('reports/' + DAY)
    return processor, downloads


def test_s3_import_loads_completion_once_for_an_empty_day(monkeypatch, database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    processor, downloads = run_s3_import(monkeypatch, database)
    assert processor.failed_tasks == []
    assert len(downloads) == 2
    assert database.connection.raw.execute('SELECT COUNT(*) FROM firebase_event_daily').fetchone()[0] == 0
    assert database.connection.raw.execute('SELECT app_id FROM firebase_collection_daily').fetchone()[0] == APP


@pytest.mark.parametrize('failure', ['corrupt', 'AccessDenied'])
def test_s3_manifest_failure_keeps_previous_data(monkeypatch, database, failure):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    processor, _ = run_s3_import(
        monkeypatch, database,
        corrupt_hash=failure == 'corrupt',
        manifest_error='AccessDenied' if failure == 'AccessDenied' else None,
    )
    assert len(processor.failed_tasks) == 1
    assert database.connection.raw.execute('SELECT event_count FROM firebase_event_daily').fetchone()[0] == 10
    assert database.connection.raw.execute('SELECT source_sha256 FROM firebase_collection_daily').fetchone()[0] == 'a' * 64


def test_missing_s3_manifest_does_not_leave_stale_success(monkeypatch, database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    processor, _ = run_s3_import(monkeypatch, database, manifest_error='NoSuchKey')
    assert processor.failed_tasks == []
    assert database.connection.raw.execute('SELECT COUNT(*) FROM firebase_collection_daily').fetchone()[0] == 0


def test_summary_import_is_separate_and_empty_day_is_confirmed(monkeypatch, database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64)
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64, table_name='firebase_app_event_daily')
    processor, downloads = run_s3_import(monkeypatch, database, summary=True)
    assert not processor.failed_tasks
    assert len(downloads) == 2
    assert database.connection.raw.execute('SELECT COUNT(*) FROM firebase_app_event_daily').fetchone()[0] == 0
    assert database.connection.raw.execute('SELECT app_id FROM firebase_app_collection_daily').fetchone()[0] == APP
    assert database.connection.raw.execute('SELECT event_count FROM firebase_event_daily').fetchone()[0] == 10


@pytest.mark.parametrize('failure', ['missing', 'corrupt', 'unverified'])
def test_summary_import_requires_verified_matching_completion(monkeypatch, database, failure):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64, table_name='firebase_app_event_daily')
    processor, _ = run_s3_import(
        monkeypatch, database, summary=True,
        manifest_error='NoSuchKey' if failure == 'missing' else None,
        corrupt_hash=failure == 'corrupt', quality_verified=failure != 'unverified',
    )
    assert len(processor.failed_tasks) == 1
    assert database.connection.raw.execute('SELECT event_count FROM firebase_app_event_daily').fetchone()[0] == 10
    assert database.connection.raw.execute('SELECT source_sha256 FROM firebase_app_collection_daily').fetchone()[0] == 'a' * 64


@pytest.mark.parametrize('event,version,country', [('(other)', '', ''), ('first_open', '1.3', ''), ('first_open', '', 'US')])
def test_summary_rejects_collapsed_or_detail_rows(tmp_path, event, version, country):
    body = HEADER + f'{DAY},{event},iOS,,{version},{country},4,5,5,202,{APP}\n'
    path, _ = write_pair(tmp_path, body)
    with pytest.raises(ValueError, match='Invalid Firebase app/event summary row'):
        FirebaseAppEventProcessor().process_data(str(path))


def test_summary_rejects_duplicate_grains(tmp_path):
    row = f'{DAY},first_open,iOS,,,,4,5,5,202,{APP}\n'
    path, _ = write_pair(tmp_path, HEADER + row + row)
    with pytest.raises(ValueError, match='Duplicate'):
        FirebaseAppEventProcessor().process_data(str(path))


def test_summary_database_failure_rolls_back_both_tables(database):
    database.replace_firebase_day(DAY, [sample_report()], {'202': APP}, 'a' * 64, table_name='firebase_app_event_daily')
    with pytest.raises(sqlite3.IntegrityError):
        database.replace_firebase_day(DAY, [], {'202': APP}, 'bad-hash', table_name='firebase_app_event_daily')
    assert database.connection.raw.execute('SELECT event_count FROM firebase_app_event_daily').fetchone()[0] == 10
