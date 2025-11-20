import json
import urllib.request
from typing import Optional
from src.util.config import Config
from src.util.logger import get_logger


logger = get_logger("slack_notifier")


class SlackNotifier:
    
    def __init__(self, config: Config):
        self.config = config
        self.webhook_url = self._get_slack_webhook_url()
    
    def _get_slack_webhook_url(self) -> Optional[str]:
        return (
            getattr(self.config, 'slack_webhook_url', None)
        )
    
    def _get_from_env(self, key: str) -> Optional[str]:
        import os
        return os.environ.get(key)
    
    def send_alert(self, message: str, title: str = "ADN Report Processor Alert") -> bool:
        if not self.webhook_url:
            logger.warning("Slack webhook URL not configured, skipping notification")
            return False
        
        try:
            payload = {
                "text": title,
                "attachments": [
                    {
                        "color": "danger",
                        "fields": [
                            {
                                "title": "Load ADN report to mysql error ",
                                "value": message,
                                "short": False
                            }
                        ]
                    }
                ]
            }

            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    logger.info("Slack alert sent successfully")
                    return True
                else:
                    logger.error(f"Failed to send Slack alert, status: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending Slack alert: {str(e)}")
            return False
    
    def send_success_notification(self, message: str, title: str = "ADN Report Processor Success") -> bool:
        if not self.webhook_url:
            logger.warning("Slack webhook URL not configured, skipping notification")
            return False
        
        try:
            payload = {
                "text": title,
                "attachments": [
                    {
                        "color": "good",
                        "fields": [
                            {
                                "title": "Details",
                                "value": message,
                                "short": False
                            }
                        ]
                    }
                ]
            }

            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req) as response:
                if response.status == 200:
                    logger.info("Slack notification sent successfully")
                    return True
                else:
                    logger.error(f"Failed to send Slack notification, status: {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"Error sending Slack notification: {str(e)}")
            return False