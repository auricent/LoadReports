from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class CpmstarReport(ReportData):
    country: str
    pool_id: int
    pool_name: str
    clicks: int
    impressions: int
    revenue: float
    actions: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "country": self.country,
            "pool_id": self.pool_id,
            "pool_name": self.pool_name,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue,
            "actions": self.actions
        }