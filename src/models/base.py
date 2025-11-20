from dataclasses import dataclass
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from datetime import date, datetime


@dataclass
class ReportData(ABC):
    day: date
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass