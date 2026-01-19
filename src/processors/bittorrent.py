import csv
import logging
from datetime import datetime
from typing import List, Optional
from src.models.bittorrent import BittorrentInstallerReport
from src.models.base import ReportData
from src.processors.base import ReportProcessor


class BittorrentInstallerProcessor(ReportProcessor):
    
    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []
        
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):
                try:
                    # 解析日期
                    day_str = row.get('Date', '1970-01-01')
                    day = datetime.strptime(day_str, '%Y-%m-%d').date()
                    
                    report = BittorrentInstallerReport(
                        day=day,
                        installer_name=row.get('Installer Name', ''),
                        geo=row.get('Geo', ''),
                        installation_started=self._parse_int(row.get('Installation Started', 0)),
                        installer_success_rate=self._parse_float(row.get('lnstaller Success Rate')),
                        installer_error_rate=self._parse_float(row.get('lnstaller Error Rate')),
                        installer_quit_rate=self._parse_float(row.get('Installer Quit Rate')),
                        revenue_per_started=self._parse_float(row.get('Revenue Per Started')),
                        offers_made=self._parse_int(row.get('Offers Made', 0)),
                        offers_installs=self._parse_int(row.get('Offers Installs', 0)),
                        revenue=self._parse_float(row.get('Revenue')),
                        installation_completed=self._parse_int(row.get('Installation Completed', 0)),
                        revenue_per_completed=self._parse_float(row.get('Revenue Per Completed'))
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))
        
        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")
        
        return reports
    
    def _parse_int(self, value) -> int:
        """解析整数，空值返回0"""
        if value is None or value == '':
            return 0
        return int(value)
    
    def _parse_float(self, value) -> Optional[float]:
        """解析浮点数，空值返回None"""
        if value is None or value == '':
            return None
        return float(value)
    
    def get_target_table(self) -> str:
        return "bittorrent_installer_report"
