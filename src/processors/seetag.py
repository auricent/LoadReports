import csv
import logging
from datetime import datetime
from typing import List
from src.models.base import ReportData
from src.models.seetag import SeetagReport
from src.processors.base import ReportProcessor


class SeetagReportProcessor(ReportProcessor):

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []

        with open(file_path, 'r', encoding='utf-8-sig', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            required_fields = {'day', 'publisher_name', 'ad_type', 'country', 'clicks', 'impressions', 'revenue'}
            missing_fields = required_fields - set(reader.fieldnames or [])
            if missing_fields:
                raise ValueError(f"Missing required columns: {', '.join(sorted(missing_fields))}")

            for row_num, row in enumerate(reader, start=2):
                try:
                    day = datetime.strptime(row['day'], '%Y-%m-%d').date()

                    report = SeetagReport(
                        day=day,
                        publisher_name=row['publisher_name'],
                        ad_type=row['ad_type'],
                        country=row['country'],
                        clicks=int(row['clicks'] or 0),
                        impressions=int(row['impressions'] or 0),
                        revenue=float(row['revenue'] or 0.0)
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))

        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")

        return reports

    def get_target_table(self) -> str:
        return "seedtag_report"
