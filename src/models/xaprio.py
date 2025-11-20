from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class XaprioReport(ReportData):
    zone_id: int
    zone_name: str
    requests: int
    coverage: int
    clicks: int
    impressions: int
    revenue: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "zone_id": self.zone_id,
            "zone_name": self.zone_name,
            "requests": self.requests,
            "coverage": self.coverage,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue
        }