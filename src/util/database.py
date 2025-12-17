from typing import List, Dict, Any
from src.util.config import DatabaseConfig
from src.models import ReportData
from src.util.logger import get_logger
import mysql.connector


MYSQL_CONNECTOR = mysql.connector
logger = get_logger("database")


class DatabaseClient:
    
    def __init__(self, config: DatabaseConfig):
        if MYSQL_CONNECTOR is None:
            raise ImportError("mysql-connector-python is not installed")
        
        self.config = config
        self.connection = None
    
    def connect(self):
        logger.info("Connecting to database")
        self.connection = MYSQL_CONNECTOR.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.username,
            password=self.config.password,
            database=self.config.database
        )
        logger.info("Database connected successfully")
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")
    
    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        if not self.connection or not self.connection.is_connected():
            raise Exception("Database not connected")
        
        if not data:
            logger.warning("No data to insert")
            return
        
        cursor = self.connection.cursor()

        columns = list(data[0].keys())
        placeholders = ', '.join(['%s'] * len(columns))
        column_names = ', '.join([f"`{col}`" for col in columns])
        sql = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"

        values = [tuple(row[col] for col in columns) for row in data]
        cursor.executemany(sql, values)
        self.connection.commit()
        cursor.close()
        logger.info(f"Inserted {len(data)} records into {table_name}")
    
    def delete_data(self, table_name: str, date_column: str, date_value: str) -> None:
        if not self.connection or not self.connection.is_connected():
            raise Exception("Database not connected")

        cursor = self.connection.cursor()

        sql = f"DELETE FROM {table_name} WHERE {date_column} = %s"

        cursor.execute(sql, (date_value,))
        deleted_rows = cursor.rowcount
        self.connection.commit()
        cursor.close()
        logger.info(f"Deleted {deleted_rows} records from {table_name} for {date_column} = {date_value}")

    def delete_agg_data(self, table_name: str, adn_network: str, date_column: str, date_value: str) -> None:
        if not self.connection or not self.connection.is_connected():
            raise Exception("Database not connected")

        cursor = self.connection.cursor()

        sql = f"DELETE FROM {table_name} WHERE {date_column} = %s and adn_network= %s"

        cursor.execute(sql, (date_value,adn_network))
        deleted_rows = cursor.rowcount
        self.connection.commit()
        cursor.close()
        logger.info(f"Deleted {deleted_rows} records from {table_name} for {date_column} = {date_value} and adn_network = {adn_network}")
    
    def batch_insert_reports(self, table_name: str, reports: List[ReportData]) -> None:
        logger.info(f"Batch inserting {len(reports)} reports into {table_name}")
        data_dicts = [report.to_dict() for report in reports]
        self.insert_data(table_name, data_dicts)