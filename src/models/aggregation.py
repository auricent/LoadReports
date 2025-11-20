from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class AggregationRevenueReport(ReportData):
    adn_network: str
    country: str
    platform: str
    app_id: int
    app_name: str
    unit_id: str
    unit_name: str
    device_type: str
    os_type: str
    ad_type: str
    ad_size: str
    revenue: float
    requests: int
    responses: int
    clicks: int
    impressions: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "adn_network": self.adn_network,
            "day": self.day,
            "country": self.country,
            "platform": self.platform,
            "app_id": self.app_id,
            "app_name": self.app_name,
            "unit_id": self.unit_id,
            "unit_name": self.unit_name,
            "device_type": self.device_type,
            "os_type": self.os_type,
            "ad_type": self.ad_type,
            "ad_size": self.ad_size,
            "revenue": self.revenue,
            "requests": self.requests,
            "responses": self.responses,
            "clicks": self.clicks,
            "impressions": self.impressions
        }