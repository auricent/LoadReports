from typing import List
from src.util.config import S3Config
from src.util.logger import get_logger
import boto3

BOTO3 = boto3
logger = get_logger("s3_client")


class S3Client:
    
    def __init__(self, config: S3Config):
        if BOTO3 is None:
            raise ImportError("boto3 is not installed")
            
        self.config = config
        self.client = BOTO3.client(
            's3',
            region_name=config.region_name,
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key
        )
        logger.info("S3 client initialized")
    
    def list_files(self, prefix: str = '') -> List[str]:
        logger.info(f"Listing files with prefix: {prefix}")
        response = self.client.list_objects_v2(
            Bucket=self.config.bucket_name,
            Prefix=prefix
        )
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append(obj['Key'])
        
        logger.info(f"Found {len(files)} files")
        return files
    
    def download_file(self, s3_key: str, local_path: str) -> None:
        logger.info(f"Downloading {s3_key} to {local_path}")
        self.client.download_file(
            self.config.bucket_name,
            s3_key,
            local_path
        )
        logger.info(f"Download completed: {s3_key}")