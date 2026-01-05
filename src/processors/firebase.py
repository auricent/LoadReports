import csv
import logging
from datetime import datetime
from typing import List
from src.models.base import ReportData
from src.models.firebase import FirebaseReport
from src.processors.base import ReportProcessor


class FirebaseProcessor(ReportProcessor):

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = FirebaseReport(
                        day=day,
                        events=row.get('events', 0),
                        users=row.get('users', 0)
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Skipping invalid row: {row}. Error: {e}")

        return reports

    def get_target_table(self) -> str:
        return "firebase"