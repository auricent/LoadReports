from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class DidnaReport(ReportData):
    property: str
    ad_type: int
    requests: int
    impressions: int
    revenue: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "property": self.property,
            "ad_type": self.ad_type,
            "requests": self.requests,
            "impressions": self.impressions,
            "revenue": self.revenue
        }