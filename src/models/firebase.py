from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class FirebaseReport(ReportData):
    event_name: str
    platform: str
    operating_system: str
    app_version: str
    country: str
    event_count: int
    total_users: int
    active_users: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "event_name": self.event_name,
            "platform": self.platform,
            "operating_system": self.operating_system,
            "app_version": self.app_version,
            "country": self.country,
            "event_count": self.event_count,
            "total_users": self.total_users,
            "active_users": self.active_users
        }
