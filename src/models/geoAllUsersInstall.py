from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class GeoAllUsersInstallReport(ReportData):
    app: str
    users: int
    country: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "app": self.app,
            "users": self.users,
            "country": self.country
        }