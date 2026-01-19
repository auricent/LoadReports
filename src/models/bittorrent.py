from dataclasses import dataclass
from typing import Dict, Any, Optional
from src.models.base import ReportData


@dataclass
class BittorrentInstallerReport(ReportData):
    installer_name: str
    geo: str
    installation_started: int
    installer_success_rate: Optional[float]
    installer_error_rate: Optional[float]
    installer_quit_rate: Optional[float]
    revenue_per_started: Optional[float]
    offers_made: int
    offers_installs: int
    revenue: Optional[float]
    installation_completed: int
    revenue_per_completed: Optional[float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "installer_name": self.installer_name,
            "geo": self.geo,
            "installation_started": self.installation_started,
            "installer_success_rate": self.installer_success_rate,
            "installer_error_rate": self.installer_error_rate,
            "installer_quit_rate": self.installer_quit_rate,
            "revenue_per_started": self.revenue_per_started,
            "offers_made": self.offers_made,
            "offers_installs": self.offers_installs,
            "revenue": self.revenue,
            "installation_completed": self.installation_completed,
            "revenue_per_completed": self.revenue_per_completed
        }
