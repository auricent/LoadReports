import os
from typing import Dict
from src.processors.bidmatic import BidmaticReportProcessor
from src.processors.aggregation import AggregationReportProcessor
from src.processors.didna import DidnaReportProcessor
from src.processors.cpmstar import CpmstarReportProcessor
from src.processors.xaprio import XaprioReportProcessor
from src.processors.smartadserver import SmartAdServerReportProcessor
from src.processors.freewheel import FreewheelReportProcessor
from src.processors.applovin import ApplovinMaxReportProcessor
from src.util.s3_client import S3Client
from src.util.database import DatabaseClient
from src.util.logger import get_logger

logger = get_logger("processor")


class DataProcessor:
    
    def __init__(self, s3_client: S3Client, db_client: DatabaseClient):
        self.s3_client = s3_client
        self.db_client = db_client
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

            if file_name in self.processors:
                processor, table_name = self.processors[file_name]
                logger.info(f"Using processor for {file_name}, target table: {table_name}")

                local_path = f"/tmp/{file_name}"
                self.s3_client.download_file(file_key, local_path)

                reports = processor.process_data(local_path)

                if reports:
                    date_str = s3_prefix.split("/")[-1]
                    logger.info(f"delete data of  {table_name} in {date_str}")
                    self.db_client.delete_data(table_name, 'day', date_str)

                    logger.info(f"Inserting {len(reports)} reports into {table_name}")
                    self.db_client.batch_insert_reports(table_name, reports)
                else:
                    logger.info(f"No reports to insert for {file_name}")

                # os.remove(local_path)
                logger.info(f"Finished processing {file_name}")
            else:
                logger.warning(f"No processor found for file: {file_name}")