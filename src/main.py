import datetime
from src.util.config import Config
from src.util.s3_client import S3Client
from src.util.database import DatabaseClient
from src.processors.processor import DataProcessor
from src.util.slack_notifier import SlackNotifier
from src.util.logger import get_logger
import argparse


def main(start_date_str=None, end_date_str=None, file_filter=None):
    logger = get_logger("main")
    logger.info("Starting ADN Report Processor")

    config = Config.load()
    logger.info("Configuration loaded successfully")

    slack_notifier = SlackNotifier(config)
    
    try:
        s3_client = S3Client(config.s3)
        db_client = DatabaseClient(config.db)
        
        # 初始化外部 S3 客户端 (用于 bittorrent installer 等)
        s3_external_client = None
        if config.s3_external:
            s3_external_client = S3Client(config.s3_external)
            logger.info("External S3 client initialized")
        
        logger.info("Clients initialized")

        db_client.connect()
        logger.info("Database connected")
        
        try:
            processor = DataProcessor(s3_client, db_client, slack_notifier, file_filter=file_filter)

            if start_date_str is None or end_date_str is None:
                today = datetime.date.today()
                date_string = today.strftime("%Y-%m-%d")
                processor.process_s3_files(f"reports/{date_string}")
                
                # 处理 bittorrent installer 报告
                if s3_external_client:
                    processor.process_bittorrent_file(s3_external_client, date_string)
            else:
                # 转成 date 类型
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

                # 日期范围循环（包含 end）
                current_date = start_date
                while current_date <= end_date:
                    date_string = current_date.strftime("%Y-%m-%d")
                    processor.process_s3_files(f"reports/{date_string}")
                    
                    # 处理 bittorrent installer 报告
                    if s3_external_client:
                        processor.process_bittorrent_file(s3_external_client, date_string)
                    
                    processor.clear_failed_tasks()  # 每天处理完后清空，下一天重新统计
                    current_date += datetime.timedelta(days=1)

            logger.info("Data processing completed")

        finally:
            db_client.disconnect()
            logger.info("Database disconnected")
            
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        logger.error(error_message, exc_info=True)
        slack_notifier.send_alert(error_message)
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--start", type=str, required=False)
    parser.add_argument("--end", type=str, required=False)
    parser.add_argument("--file", type=str, required=False, help="只处理指定文件，如 HTX_data.csv")

    args = parser.parse_args()

    main(args.start, args.end, args.file)