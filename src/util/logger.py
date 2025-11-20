import os
import logging
from typing import Optional


class LoggerManager:
    _instance = None
    _logger: Optional[logging.Logger] = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance

    def initialize(self, log_level=logging.INFO, log_file_name="adn_report.log") -> logging.Logger:
        if self._initialized and self._logger is not None:
            return self._logger
            
        log_dir = "/tmp/app/logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, log_file_name)),
                logging.StreamHandler()
            ]
        )
        
        self._logger = logging.getLogger("adn_report")
        self._initialized = True
        return self._logger

    def get_logger(self, name=None) -> logging.Logger:
        if not self._initialized or self._logger is None:
            return self.initialize()
            
        if name:
            return logging.getLogger(f"adn_report.{name}")
        return self._logger


logger_manager = LoggerManager()

def get_logger(name=None) -> logging.Logger:
    return logger_manager.get_logger(name)