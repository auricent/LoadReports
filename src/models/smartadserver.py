from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class SmartAdServerReport(ReportData):
    country: str
    clicks: int
    impressions: int
    revenue: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "country": self.country,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue
        }