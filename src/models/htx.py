from dataclasses import dataclass
from typing import Dict, Any
from datetime import date
from src.models.base import ReportData


@dataclass
class HtxReport(ReportData):
    insertion_name: str
    insertion_id: int
    impressions: int
    clicks: int
    viewable_impressions: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "insertion_name": self.insertion_name,
            "insertion_id": self.insertion_id,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "viewable_impressions": self.viewable_impressions
        }
