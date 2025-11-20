from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class ApplovinMaxReport(ReportData):
    ad_format: str
    application: str
    attempts: int
    country: str
    device_type: int
    estimated_revenue: float
    impressions: int
    max_ad_unit_name: str
    max_ad_unit_id: str
    platform: int
    responses: int
    network: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "ad_format": self.ad_format,
            "application": self.application,
            "attempts": self.attempts,
            "country": self.country,
            "device_type": self.device_type,
            "estimated_revenue": self.estimated_revenue,
            "impressions": self.impressions,
            "max_ad_unit_name": self.max_ad_unit_name,
            "max_ad_unit_id": self.max_ad_unit_id,
            "platform": self.platform,
            "responses": self.responses,
            "network": self.network
        }