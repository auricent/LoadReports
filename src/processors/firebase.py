import csv
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

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
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
                        active_users=parse_int(row.get('active_users'))
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
