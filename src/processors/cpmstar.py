import csv
from datetime import datetime
from typing import List
from src.models.cpmstar import CpmstarReport
from src.models.base import ReportData
from src.processors.base import ReportProcessor


class CpmstarReportProcessor(ReportProcessor):
    
    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()

                    report = CpmstarReport(
                        day=day,
                        country=row.get('country', ''),
                        ad_type=row.get("ad_type",0),
                        pool_id=int(row.get('pool_id', 0)),
                        pool_name=row.get('pool_name', ''),
                        clicks=int(row.get('clicks', 0)),
                        impressions=int(row.get('impressions', 0)),
                        revenue=float(row.get('revenue', 0.0)),
                        actions=int(row.get('actions', 0))
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid row: {row}. Error: {e}")
        
        return reports
    
    def get_target_table(self) -> str:
        return "cpmstar_report"