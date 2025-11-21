from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class SmartAdServerReport(ReportData):
    country: str
    auctions: int
    clicks: int
    impressions: int
    revenue: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "country": self.country,
            "auctions": self.auctions,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue
        }