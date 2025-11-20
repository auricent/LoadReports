import datetime
from src.util.config import Config
from src.util.s3_client import S3Client
from src.util.database import DatabaseClient
from src.processors.processor import DataProcessor
from src.util.slack_notifier import SlackNotifier
from src.util.logger import get_logger


def main():
    logger = get_logger("main")
    logger.info("Starting ADN Report Processor")

    config = Config.load()
    logger.info("Configuration loaded successfully")

    slack_notifier = SlackNotifier(config)
    
    try:
        s3_client = S3Client(config.s3)
        db_client = DatabaseClient(config.db)
        logger.info("Clients initialized")

        db_client.connect()
        logger.info("Database connected")
        
        try:
            processor = DataProcessor(s3_client, db_client)

            today = datetime.date.today()
            date_string = today.strftime("%Y-%m-%d")

            processor.process_s3_files(f"reports/{date_string}")
            logger.info("Data processing completed successfully")

        finally:
            db_client.disconnect()
            logger.info("Database disconnected")
            
    except Exception as e:
        error_message = f"Error occurred: {str(e)}"
        logger.error(error_message, exc_info=True)
        slack_notifier.send_alert(error_message)
        raise


if __name__ == "__main__":
    main()