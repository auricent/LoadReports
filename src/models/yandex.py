from dataclasses import dataclass
from typing import Dict, Any
from src.models.base import ReportData


@dataclass
class YandexReport(ReportData):
    unit_name: str
    country: str
    requests: int
    clicks: int
    impressions: int
    revenue: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "unit_name": self.unit_name,
            "country": self.country,
            "requests": self.requests,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue
        }