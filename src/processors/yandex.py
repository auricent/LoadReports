import csv
import logging
from datetime import datetime
from typing import List
from src.models.base import ReportData
from src.models.yandex import YandexReport
from src.processors.base import ReportProcessor


class YandexReportProcessor(ReportProcessor):

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = YandexReport(
                        day=day,
                        unit_name=row.get('unit_name', ''),
                        country=row.get('country', ''),
                        requests=int(row.get('requests', 0)),
                        clicks=int(row.get('clicks', 0)),
                        impressions=int(row.get('impressions', 0)),
                        revenue=float(row.get('revenue', 0.0))
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Skipping invalid row: {row}. Error: {e}")

        return reports

    def get_target_table(self) -> str:
        return "yandex_report"