from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class FreewheelReport(ReportData):
    country: str
    publisher_id: int
    zone_id: int
    requests: int
    clicks: int
    impressions: int
    revenue: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "country": self.country,
            "publisher_id": self.publisher_id,
            "zone_id": self.zone_id,
            "requests": self.requests,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue
        }