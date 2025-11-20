from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class BidmaticReport(ReportData):
    country: str
    ad_type: int
    domain: str
    os: str
    ad_requests: int
    ad_opportunities: int
    impressions_good: int
    revenue: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "country": self.country,
            "ad_type": self.ad_type,
            "domain": self.domain,
            "os": self.os,
            "ad_requests": self.ad_requests,
            "ad_opportunities": self.ad_opportunities,
            "impressions_good": self.impressions_good,
            "revenue": self.revenue
        }