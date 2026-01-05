from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class FirebaseReport(ReportData):
    events: int
    users: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "events": self.events,
            "users": self.users
        }