from dataclasses import dataclass
from typing import Dict, Any
from src.models.base import ReportData


@dataclass
class SeetagReport(ReportData):
    publisher_name: str
    ad_type: str
    clicks: int
    impressions: int
    revenue: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "publisher_name": self.publisher_name,
            "ad_type": self.ad_type,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue
        }