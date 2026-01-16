import csv
import logging
from datetime import datetime
from typing import List
from src.models.aggregation import AggregationRevenueReport
from src.models.base import ReportData
from src.processors.base import ReportProcessor


class AggregationReportProcessor(ReportProcessor):
    
    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):
                try:
                    day_str = row.get('day', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()
                    
                    report = AggregationRevenueReport(
                        adn_network=row.get('adn_network', ''),
                        day=day,
                        country=row.get('country', ''),
                        platform=row.get('platform', ''),
                        app_id=int(row.get('app_id', 0)),
                        app_name=row.get('app_name', ''),
                        unit_id=row.get('unit_id', ''),
                        unit_name=row.get('unit_name', ''),
                        device_type=row.get('device_type', ''),
                        os_type=row.get('os_type', ''),
                        ad_type=row.get('ad_type', ''),
                        ad_size=row.get('ad_size', ''),
                        revenue=float(row.get('revenue', 0.0)),
                        requests=int(row.get('requests', 0)),
                        responses=int(row.get('responses', 0)),
                        clicks=int(row.get('clicks', 0)),
                        impressions=int(row.get('impressions', 0))
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))
        
        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")
        
        return reports
    
    def get_target_table(self) -> str:
        return "adn_aggregation_revenue_report"