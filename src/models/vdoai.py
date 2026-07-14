from dataclasses import dataclass
from typing import Dict, Any
from datetime import date

from src.models.base import ReportData


@dataclass
class VdoaiReport(ReportData):
    website: str
    tag: str
    revenue: float
    unit_pageview_match: int
    pageview_match: int
    viewability: float
    matched_pageview_cpm: float
    unit_matched_pageview_cpm: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dt": self.day,
            "website": self.website,
            "tag": self.tag,
            "revenue": self.revenue,
            "unit_pageview_match": self.unit_pageview_match,
            "pageview_match": self.pageview_match,
            "viewability": self.viewability,
            "matched_pageview_cpm": self.matched_pageview_cpm,
            "unit_matched_pageview_cpm": self.unit_matched_pageview_cpm,
        }
