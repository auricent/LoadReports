import unittest
from unittest.mock import patch, MagicMock
from src.util.slack_notifier import SlackNotifier
from src.util.config import Config, S3Config, DatabaseConfig


class TestSlackNotifier(unittest.TestCase):
    
    def setUp(self):
        s3_config = S3Config(
            bucket_name="test_bucket",
            region_name="us-east-1"
        )
        
        db_config = DatabaseConfig(
            host="localhost",
            port=3306,
            username="test_user",
            password="test_password",
            database="test_db"
        )
        
        self.config = Config(
            s3=s3_config,
            db=db_config,
            slack_webhook_url="https://hooks.slack.com/services/test/webhook/url"
        )
    
    def test_init_with_webhook_url(self):
        notifier = SlackNotifier(self.config)
        self.assertEqual(notifier.webhook_url, "https://hooks.slack.com/services/test/webhook/url")
    
    def test_init_without_webhook_url(self):
        config = Config(
            s3=S3Config(bucket_name="test_bucket"),
            db=DatabaseConfig(host="localhost", port=3306, username="user", password="pass", database="db")
        )
        notifier = SlackNotifier(config)
        self.assertIsNone(notifier.webhook_url)
    
    @patch('urllib.request.urlopen')
    def test_send_alert_success(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        notifier = SlackNotifier(self.config)
        result = notifier.send_alert("Test error message", "Test Alert")
        
        self.assertTrue(result)
        mock_urlopen.assert_called_once()
    
    @patch('urllib.request.urlopen')
    def test_send_alert_failure(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 500
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        notifier = SlackNotifier(self.config)
        result = notifier.send_alert("Test error message", "Test Alert")
        
        self.assertFalse(result)
        mock_urlopen.assert_called_once()
    
    @patch('urllib.request.urlopen')
    def test_send_alert_exception(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network error")
        
        notifier = SlackNotifier(self.config)
        result = notifier.send_alert("Test error message", "Test Alert")
        
        self.assertFalse(result)
    
    def test_send_alert_no_webhook_url(self):
        config = Config(
            s3=S3Config(bucket_name="test_bucket"),
            db=DatabaseConfig(host="localhost", port=3306, username="user", password="pass", database="db")
        )
        notifier = SlackNotifier(config)
        result = notifier.send_alert("Test error message", "Test Alert")
        
        self.assertFalse(result)
    
    @patch('urllib.request.urlopen')
    def test_send_success_notification(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        notifier = SlackNotifier(self.config)
        result = notifier.send_success_notification("Process completed successfully", "Success Notification")
        
        self.assertTrue(result)
        mock_urlopen.assert_called_once()


if __name__ == '__main__':
    unittest.main()