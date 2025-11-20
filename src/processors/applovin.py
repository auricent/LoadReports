import csv
import logging
from datetime import datetime
from typing import List
from src.models.applovin import ApplovinMaxReport
from src.models.base import ReportData
from src.processors.base import ReportProcessor


class ApplovinMaxReportProcessor(ReportProcessor):
    
    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = ApplovinMaxReport(
                        day=day,
                        ad_format=row.get('ad_format', ''),
                        application=row.get('application', ''),
                        attempts=int(row.get('attempts', 0)),
                        country=row.get('country', ''),
                        device_type=int(row.get('device_type', 0)),
                        estimated_revenue=float(row.get('estimated_revenue', 0.0)),
                        impressions=int(row.get('Impressions', 0)),
                        max_ad_unit_name=row.get('max_ad_unit_name', ''),
                        max_ad_unit_id=row.get('max_ad_unit_id', ''),
                        platform=int(row.get('platform', 1)),
                        responses=int(row.get('responses', 0)),
                        network=row.get('network', '')
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Skipping invalid row: {row}. Error: {e}")
        
        return reports
    
    def get_target_table(self) -> str:
        return "applovin_max_report"