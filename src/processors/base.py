from abc import ABC, abstractmethod
from typing import List
from src.models.base import ReportData


class ReportProcessor(ABC):
    
    @abstractmethod
    def process_data(self, file_path: str) -> List[ReportData]:
        pass
    
    @abstractmethod
    def get_target_table(self) -> str:
        pass