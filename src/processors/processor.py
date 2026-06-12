import os
import re
import traceback
from typing import Dict, Optional, List

from src.processors.allUsersInstall import AllUsersInstallProcessor
from src.processors.bidmatic import BidmaticReportProcessor
from src.processors.aggregation import AggregationReportProcessor
from src.processors.bittorrent import BittorrentInstallerProcessor
from src.processors.didna import DidnaReportProcessor
from src.processors.cpmstar import CpmstarReportProcessor
from src.processors.firebase import FirebaseProcessor
from src.processors.geoAllUsersInstall import GeoAllUsersInstallProcessor
from src.processors.newUsersInstall import NewUsersInstallProcessor
from src.processors.seetag import SeetagReportProcessor
from src.processors.xaprio import XaprioReportProcessor
from src.processors.smartadserver import SmartAdServerReportProcessor
from src.processors.freewheel import FreewheelReportProcessor
from src.processors.applovin import ApplovinMaxReportProcessor
from src.processors.yandex import YandexReportProcessor
from src.processors.paypro import PayproReportProcessor
from src.processors.usatoday import UsaTodayReportProcessor
from src.processors.htx import HtxReportProcessor
from src.util.s3_client import S3Client
from src.util.database import DatabaseClient
from src.util.logger import get_logger

logger = get_logger("processor")


class DataProcessor:

    agg_deleted = False
    
    def __init__(self, s3_client: S3Client, db_client: DatabaseClient, slack_notifier=None, file_filter: str = None):
        self.s3_client = s3_client
        self.db_client = db_client
        self.slack_notifier = slack_notifier
        self.file_filter = file_filter
        self.failed_tasks: List[Dict] = []  # 记录失败的任务
        self.processors: Dict[str, tuple] = {
            "applovinMax.csv": (ApplovinMaxReportProcessor(), 'applovin_max_report'),
            'applovinMax_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'bidmatic.csv': (BidmaticReportProcessor(), 'bidmatic_report'),
            'bidmatic_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'didna.csv': (DidnaReportProcessor(), 'didna_report'),
            'didna_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'cpmstar.csv': (CpmstarReportProcessor(), 'cpmstar_report'),
            'cpmstar_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'xaprio.csv': (XaprioReportProcessor(), 'xaprio_report'),
            'xaprio_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'smartadserver.csv': (SmartAdServerReportProcessor(), 'smartAdServer_report'),
            'smartadserver_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'freewheel.csv': (FreewheelReportProcessor(), 'freewheel_report'),
            'freewheel_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'yandex.csv': (YandexReportProcessor(),'yandex_report'),
            'yandex_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'seedtag.csv': (SeetagReportProcessor(),'seedtag_report'),
            'seedtag_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'paypro.csv': (PayproReportProcessor(), 'paypro_report'),
            'usaToday.csv': (UsaTodayReportProcessor(), 'usa_today_report'),
            'usaToday_aggregation.csv': (AggregationReportProcessor(), 'adn_aggregation_revenue_report'),
            'HTX_data.csv': (HtxReportProcessor(), 'htx_report'),
            'firebase_event_dimensions_daily.csv': (FirebaseProcessor(), 'firebase_event_dimensions_daily'),
            # 'all-users-install.csv': (AllUsersInstallProcessor(), 'google_play_all_users_install'),
            # 'new-users-install.csv': (NewUsersInstallProcessor(), 'google_play_new_users_install'),
            # 'all-countries-install.csv': (GeoAllUsersInstallProcessor(), 'google_play_all_countries_install'),
        }
    
    def register_processor(self, file_pattern: str, processor: tuple) -> None:
        self.processors[file_pattern] = processor
    
    def process_s3_files(self, s3_prefix: str = '') -> None:
        logger.info(f"Processing S3 files with prefix: {s3_prefix}")
        files = self.s3_client.list_files(s3_prefix)
        logger.info(f"Found {len(files)} files to process")
        
        for file_key in files:
            file_name = os.path.basename(file_key)
            logger.info(f"Processing file: {file_name}")

            if self.file_filter and file_name != self.file_filter:
                continue

            if file_name in self.processors:
                try:
                    self._process_single_file(file_key, file_name, s3_prefix)
                except Exception as e:
                    error_info = {
                        'file_name': file_name,
                        'file_key': file_key,
                        's3_prefix': s3_prefix,
                        'error': str(e),
                        'traceback': traceback.format_exc()
                    }
                    self.failed_tasks.append(error_info)
                    logger.error(f"Failed to process file {file_name}: {str(e)}", exc_info=True)
                    self._send_task_failure_alert(error_info)
            else:
                logger.warning(f"No processor found for file: {file_name}")
        
        # 处理完成后，如果有失败的任务，发送汇总告警
        if self.failed_tasks:
            self._send_batch_failure_summary(s3_prefix)
    
    def _process_single_file(self, file_key: str, file_name: str, s3_prefix: str) -> None:
        """处理单个文件"""
        processor, table_name = self.processors[file_name]
        logger.info(f"Using processor for {file_name}, target table: {table_name}")

        local_path = f"/tmp/{file_name}"
        self.s3_client.download_file(file_key, local_path)

        reports = processor.process_data(local_path)

        if reports:
            date_str = s3_prefix.split("/")[-1]

            if file_name.endswith('_aggregation.csv') and not self.agg_deleted:
                logger.info(f"delete data of  adn_aggregation_revenue_report in {date_str}")
                self.db_client.delete_data("adn_aggregation_revenue_report", 'day', date_str)
                self.agg_deleted=True
            elif not file_name.endswith('_aggregation.csv'):
                logger.info(f"delete data of  {table_name} in {date_str}")
                self.db_client.delete_data(table_name, 'day', date_str)

            logger.info(f"Inserting {len(reports)} reports into {table_name}")
            self.db_client.batch_insert_reports(table_name, reports)
        else:
            logger.info(f"No reports to insert for {file_name}")

        # os.remove(local_path)
        logger.info(f"Finished processing {file_name}")
    
    def _send_task_failure_alert(self, error_info: Dict) -> None:
        """发送单个任务失败告警"""
        if not self.slack_notifier:
            return
        
        message = (
            f"*文件:* `{error_info['file_name']}`\n"
            f"*S3路径:* `{error_info['file_key']}`\n"
            f"*日期:* `{error_info['s3_prefix']}`\n"
            f"*错误信息:* {error_info['error']}"
        )
        
        self.slack_notifier.send_alert(
            message=message,
            title=" ADN Report 任务处理失败"
        )
    
    def _send_batch_failure_summary(self, s3_prefix: str) -> None:
        """发送批量失败汇总告警"""
        if not self.slack_notifier:
            return
        
        failed_files = [task['file_name'] for task in self.failed_tasks]
        message = (
            f"*处理日期:* `{s3_prefix}`\n"
            f"*失败任务数:* {len(self.failed_tasks)}\n"
            f"*失败文件列表:*\n" + 
            "\n".join([f"  • `{f}`" for f in failed_files])
        )
        
        self.slack_notifier.send_alert(
            message=message,
            title=f" ADN Report 处理完成 - {len(self.failed_tasks)} 个任务失败"
        )
    
    def get_failed_tasks(self) -> List[Dict]:
        """获取失败的任务列表"""
        return self.failed_tasks
    
    def clear_failed_tasks(self) -> None:
        """清空失败任务列表"""
        self.failed_tasks = []
        self.agg_deleted = False
    
    def process_bittorrent_file(self, s3_client: S3Client, date_str: str) -> None:
        """
        处理 Bittorrent Installer 报告文件
        文件路径格式: production/bittorrent/Bittorrent__{YYYYMMDD}.csv
        """
        # 将日期格式从 YYYY-MM-DD 转换为 YYYYMMDD
        date_formatted = date_str.replace("-", "")
        file_key = f"production/bittorrent/Bittorrent__{date_formatted}.csv"
        file_name = f"Bittorrent__{date_formatted}.csv"
        
        logger.info(f"Processing Bittorrent file: {file_key}")
        
        try:
            # 下载文件
            local_path = f"/tmp/{file_name}"
            s3_client.download_file(file_key, local_path)
            
            # 处理数据
            processor = BittorrentInstallerProcessor()
            table_name = "bittorrent_installer_report"
            
            reports = processor.process_data(local_path)
            
            if reports:
                logger.info(f"delete data of {table_name} in {date_str}")
                self.db_client.delete_data(table_name, 'day', date_str)
                
                logger.info(f"Inserting {len(reports)} reports into {table_name}")
                self.db_client.batch_insert_reports(table_name, reports)
            else:
                logger.info(f"No reports to insert for {file_name}")
            
            logger.info(f"Finished processing {file_name}")
            
        except Exception as e:
            error_info = {
                'file_name': file_name,
                'file_key': file_key,
                's3_prefix': f"production/bittorrent/{date_str}",
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            self.failed_tasks.append(error_info)
            logger.error(f"Failed to process file {file_name}: {str(e)}", exc_info=True)
            self._send_task_failure_alert(error_info)
