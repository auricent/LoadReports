import csv
import logging
from datetime import datetime
from typing import List
from src.models.base import ReportData
from src.models.addTorrent import AddTorrentReport
from src.processors.base import ReportProcessor


def parse_int(value) -> int:
    if value is None or value == '':
        return 0
    return int(value)


class AddTorrentProcessor(ReportProcessor):

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = AddTorrentReport(
                        day=day,
                        events=parse_int(row.get('events')),
                        users=parse_int(row.get('users'))
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))

        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")

        return reports

    def get_target_table(self) -> str:
        return "add_torrent"
