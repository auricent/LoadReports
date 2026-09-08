from dataclasses import dataclass
from typing import Any, Dict

from src.models.base import ReportData


@dataclass
class BetweenxReport(ReportData):
    site_id: int
    requests: int
    views: int
    view_rate: float
    clicks: int
    impressions: int
    revenue: float
    revenue_usd: float
    ecpm_usd: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "site_id": self.site_id,
            "requests": self.requests,
            "views": self.views,
            "view_rate": self.view_rate,
            "clicks": self.clicks,
            "impressions": self.impressions,
            "revenue": self.revenue,
            "revenue_usd": self.revenue_usd,
            "ecpm_usd": self.ecpm_usd,
        }
