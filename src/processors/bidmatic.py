import csv
import logging
from datetime import datetime
from typing import List
from src.models.bidmatic import BidmaticReport
from src.models.base import ReportData
from src.processors.base import ReportProcessor


class BidmaticReportProcessor(ReportProcessor):
    
    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = BidmaticReport(
                        day=day,
                        country=row.get('country', ''),
                        ad_type=int(row.get('ad_type', 0)),
                        domain=row.get('domain', ''),
                        os=row.get('os', ''),
                        ad_requests=int(row.get('ad_requests', 0)),
                        ad_opportunities=int(row.get('ad_opportunities', 0)),
                        impressions_good=int(row.get('impressions_good', 0)),
                        revenue=float(row.get('revenue', 0.0))
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))
        
        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")
        
        return reports
    
    def get_target_table(self) -> str:
        return "bidmatic_report"