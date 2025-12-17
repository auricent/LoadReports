import os
import yaml
from dataclasses import dataclass
from typing import Optional


@dataclass
class S3Config:
    bucket_name: str
    region_name: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None


@dataclass
class DatabaseConfig:
    host: str
    port: int
    username: str
    password: str
    database: str


@dataclass
class Config:
    s3: S3Config
    db: DatabaseConfig
    slack_webhook_url: Optional[str] = None

    @classmethod
    def load(cls, config_path: str = "config.yaml") -> "Config":
        config_data = {}
        if os.path.exists(config_path):
            try:
                with open(config_path, "r") as f:
                    config_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Failed to load config file {config_path}: {e}")

        s3_data = config_data.get("s3", {})
        s3_config = S3Config(
            bucket_name=os.getenv("s3_bucket_name", s3_data.get("bucket_name", "")),
            region_name=os.getenv("s3_region_name", s3_data.get("region_name", "us-east-1")),
            aws_access_key_id=os.getenv("s3_aws_access_key_id", s3_data.get("aws_access_key_id")),
            aws_secret_access_key=os.getenv("s3_aws_secret_access_key", s3_data.get("aws_secret_access_key")),
        )

        db_data = config_data.get("db", {})
        db_config = DatabaseConfig(
            host=os.getenv("db_host", db_data.get("host", "localhost")),
            port=int(os.getenv("db_port", db_data.get("port", 3306))),
            username=os.getenv("db_username", db_data.get("username", "root")),
            password=os.getenv("db_password", db_data.get("password", "")),
            database=os.getenv("db_database", db_data.get("database", "adn_report")),
        )

        slack_webhook_url = os.getenv("slack_webhook_url", config_data.get("slack_webhook_url"))

        return cls(s3=s3_config, db=db_config, slack_webhook_url=slack_webhook_url)

    @classmethod
    def from_env(cls) -> "Config":
        return cls.load()