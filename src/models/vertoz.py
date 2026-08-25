from dataclasses import dataclass
from typing import Any, Dict

from src.models.base import ReportData


@dataclass
class VertozReport(ReportData):
    channel_name: str
    country: str
    cpm: float
    requests: int
    impressions: int
    revenue: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "channel_name": self.channel_name,
            "country": self.country,
            "cpm": self.cpm,
            "requests": self.requests,
            "impressions": self.impressions,
            "revenue": self.revenue,
        }
