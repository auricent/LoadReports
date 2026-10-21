import csv
import hashlib
import json
import logging
from datetime import datetime
from typing import List
from src.models.base import ReportData
from src.models.firebase import FirebaseReport
from src.processors.base import ReportProcessor


def parse_int(value) -> int:
    if value is None or value == '':
        return 0
    return int(value)


class FirebaseProcessor(ReportProcessor):

    def process_completion_manifest(self, csv_path: str, manifest_path: str, day: str, reports: List[ReportData]) -> dict:
        with open(manifest_path, 'r', encoding='utf-8') as handle:
            manifest = json.load(handle)
        with open(csv_path, 'rb') as handle:
            source_hash = hashlib.sha256(handle.read()).hexdigest()
        if manifest.get('schema_version') != 1 or manifest.get('day') != day:
            raise ValueError('Invalid Firebase completion manifest version or date')
        if manifest.get('source_sha256') != source_hash:
            raise ValueError('Firebase completion manifest does not match the event CSV')
        with open(csv_path, 'r', encoding='utf-8') as handle:
            columns = csv.DictReader(handle).fieldnames or []
        if not {'day', 'event_name', 'stream_id', 'app_id'}.issubset(columns):
            raise ValueError('Firebase completion requires a CSV with app identities')
        apps = manifest.get('apps')
        if not isinstance(apps, dict) or any(
            not isinstance(stream, str) or not stream or not isinstance(app, str) or not app
            for stream, app in apps.items()
        ):
            raise ValueError('Invalid Firebase completion app identities')
        for report in reports:
            if report.app_id and apps.get(report.stream_id) != report.app_id:
                raise ValueError('Firebase event app identity is absent from the completion manifest')
        return {'apps': apps, 'source_sha256': source_hash}

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            required = {'day', 'event_name', 'platform', 'event_count', 'total_users', 'active_users'}
            if not required.issubset(reader.fieldnames or []):
                raise ValueError('Firebase CSV is missing required columns')
            for row_num, row in enumerate(reader, start=2):
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = FirebaseReport(
                        day=day,
                        event_name=row.get('event_name', ''),
                        platform=row.get('platform', ''),
                        operating_system=row.get('operating_system', ''),
                        app_version=row.get('app_version', ''),
                        country=row.get('country', ''),
                        event_count=parse_int(row.get('event_count')),
                        total_users=parse_int(row.get('total_users')),
                        active_users=parse_int(row.get('active_users')),
                        stream_id=row.get('stream_id', ''),
                        app_id=row.get('app_id', '')
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))

        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")

        return reports

    def get_target_table(self) -> str:
        return "firebase_event_daily"


class FirebaseAppEventProcessor(FirebaseProcessor):
    """App/event summaries are independent of country/version detail reports."""

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = super().process_data(file_path)
        seen = set()
        for report in reports:
            if (not report.stream_id or not report.app_id.endswith('-macOS')
                    or not report.event_name or report.event_name == '(other)'
                    or report.platform != 'iOS'
                    or report.operating_system or report.app_version or report.country
                    or min(report.event_count, report.total_users, report.active_users) < 0):
                raise ValueError('Invalid Firebase app/event summary row')
            key = (report.day, report.stream_id, report.platform, report.event_name)
            if key in seen:
                raise ValueError('Duplicate Firebase app/event summary row')
            seen.add(key)
        return reports

    def process_completion_manifest(self, csv_path: str, manifest_path: str, day: str, reports: List[ReportData]) -> dict:
        completion = super().process_completion_manifest(csv_path, manifest_path, day, reports)
        with open(manifest_path, 'r', encoding='utf-8') as handle:
            manifest = json.load(handle)
        if manifest.get('aggregation') != 'app_event' or manifest.get('quality_verified') is not True:
            raise ValueError('Firebase app/event summary quality is not verified')
        if not completion['apps'] or any(not app.endswith('-macOS') for app in completion['apps'].values()):
            raise ValueError('Invalid Firebase app/event summary app identities')
        return completion

    def get_target_table(self) -> str:
        return 'firebase_app_event_daily'
