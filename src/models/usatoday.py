from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class UsaTodayReport(ReportData):
    ad_unit: str
    ad_exchange_impressions: int
    ad_exchange_revenue: float
    ad_exchange_ad_requests: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "ad_unit": self.ad_unit,
            "ad_exchange_impressions": self.ad_exchange_impressions,
            "ad_exchange_revenue": self.ad_exchange_revenue,
            "ad_exchange_ad_requests": self.ad_exchange_ad_requests
        }
