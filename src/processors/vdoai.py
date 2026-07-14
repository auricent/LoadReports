import csv
import logging
from datetime import datetime
from typing import List

from src.models.base import ReportData
from src.models.vdoai import VdoaiReport
from src.processors.base import ReportProcessor


class VdoaiReportProcessor(ReportProcessor):

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):
                try:
                    dt_str = row.get('dt') or row.get('day', '1970-01-01')
                    dt = datetime.strptime(dt_str, '%Y-%m-%d').date()

                    report = VdoaiReport(
                        day=dt,
                        website=row.get('website', ''),
                        tag=row.get('tag', ''),
                        revenue=float(row.get('revenue', 0.0)),
                        unit_pageview_match=int(row.get('unit_pageview_match', 0)),
                        pageview_match=int(row.get('pageview_match', 0)),
                        viewability=float(row.get('viewability', 0.0)),
                        matched_pageview_cpm=float(row.get('matched_pageview_cpm', 0.0)),
                        unit_matched_pageview_cpm=float(row.get('unit_matched_pageview_cpm', 0.0)),
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))

        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")

        return reports

    def get_target_table(self) -> str:
        return "vdoai_report"
