from dataclasses import dataclass
from typing import Dict, Any
from src.models.base import ReportData


@dataclass
class NewUsersInstallReport(ReportData):
    app: str
    users: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "app": self.app,
            "users": self.users
        }