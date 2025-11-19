import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import time
import logging
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

log = logging.getLogger("alerting")

class AlertManager:
    def __init__(self, config_path="alert_config.json"):
        self.config = self.load_config(config_path)
        self.alert_history = []
        self.slack_client = None
        if self.config.get('slack_token'):
            self.slack_client = WebClient(token=self.config['slack_token'])

    def load_config(self, config_path):
        """Load alerting configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration
            return {
                "email": {
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "from_email": "",
                    "to_emails": []
                },
                "slack": {
                    "token": "",
                    "channel": "#alerts"
                },
                "thresholds": {
                    "website_response_time_ms": 5000,
                    "synthetic_failure_count": 3,
                    "synthetic_failure_window_minutes": 5,
                    "error_rate_threshold": 0.05
                }
            }

    def check_website_alert(self, website_id, response_time, status_code):
        """Check if website monitoring triggers an alert."""
        threshold = self.config['thresholds']['website_response_time_ms']
        if response_time > threshold or status_code >= 400:
            alert = {
                "type": "website",
                "website_id": website_id,
                "message": f"Website {website_id} alert: Response time {response_time}ms, Status {status_code}",
                "timestamp": int(time.time() * 1000),
                "severity": "high" if status_code >= 500 else "medium"
            }
            self.trigger_alert(alert)
            return True
        return False

    def check_synthetic_alert(self, check_id, recent_runs):
        """Check if synthetic check failures trigger an alert."""
        threshold_count = self.config['thresholds']['synthetic_failure_count']
        window_minutes = self.config['thresholds']['synthetic_failure_window_minutes']

        # Filter runs within the time window
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        recent_failures = [
            run for run in recent_runs
            if datetime.fromtimestamp(run['timestamp'] / 1000) > cutoff_time and run['status'] == 'failure'
        ]

        if len(recent_failures) >= threshold_count:
            alert = {
                "type": "synthetic",
                "check_id": check_id,
                "message": f"Synthetic check {check_id} failed {len(recent_failures)} times in {window_minutes} minutes",
                "timestamp": int(time.time() * 1000),
                "severity": "high"
            }
            self.trigger_alert(alert)
            return True
        return False

    def check_error_rate_alert(self, entity_id, error_rate):
        """Check if error rate exceeds threshold."""
        threshold = self.config['thresholds']['error_rate_threshold']
        if error_rate > threshold:
            alert = {
                "type": "error_rate",
                "entity_id": entity_id,
                "message": f"Entity {entity_id} error rate {error_rate:.3f} exceeds threshold {threshold}",
                "timestamp": int(time.time() * 1000),
                "severity": "medium"
            }
            self.trigger_alert(alert)
            return True
        return False

    def trigger_alert(self, alert):
        """Trigger alert via configured channels."""
        log.warning(f"ALERT: {alert['message']}")

        # Add to history
        self.alert_history.append(alert)

        # Send notifications
        self.send_email_alert(alert)
        self.send_slack_alert(alert)

    def send_email_alert(self, alert):
        """Send alert via email."""
        email_config = self.config.get('email', {})
        if not email_config.get('smtp_server') or not email_config.get('to_emails'):
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['from_email']
            msg['To'] = ', '.join(email_config['to_emails'])
            msg['Subject'] = f"Instana Alert: {alert['type'].upper()} - {alert['severity'].upper()}"

            body = f"""
Instana Monitoring Alert

Type: {alert['type']}
Severity: {alert['severity']}
Time: {datetime.fromtimestamp(alert['timestamp'] / 1000)}

{alert['message']}

This is an automated alert from Instana Synthetic Monitoring v1.3.0
            """
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['username'], email_config['password'])
            text = msg.as_string()
            server.sendmail(email_config['from_email'], email_config['to_emails'], text)
            server.quit()

            log.info(f"Email alert sent to {email_config['to_emails']}")

        except Exception as e:
            log.error(f"Failed to send email alert: {str(e)}")

    def send_slack_alert(self, alert):
        """Send alert via Slack."""
        if not self.slack_client:
            return

        try:
            message = f"""
🚨 *Instana Alert* 🚨

*Type:* {alert['type']}
*Severity:* {alert['severity']}
*Time:* {datetime.fromtimestamp(alert['timestamp'] / 1000)}

{alert['message']}
            """

            self.slack_client.chat_postMessage(
                channel=self.config['slack']['channel'],
                text=message
            )

            log.info(f"Slack alert sent to {self.config['slack']['channel']}")

        except SlackApiError as e:
            log.error(f"Failed to send Slack alert: {e.response['error']}")

    def get_alert_history(self, hours=24):
        """Get recent alert history."""
        cutoff_time = int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
        return [alert for alert in self.alert_history if alert['timestamp'] > cutoff_time]

    def save_alert_history(self, filepath="alert_history.jsonl"):
        """Save alert history to file."""
        with open(filepath, 'w') as f:
            for alert in self.alert_history:
                f.write(json.dumps(alert) + '\n')

    def load_alert_history(self, filepath="alert_history.jsonl"):
        """Load alert history from file."""
        try:
            with open(filepath, 'r') as f:
                self.alert_history = [json.loads(line) for line in f]
        except FileNotFoundError:
            self.alert_history = []

# Global alert manager instance
alert_manager = AlertManager()

def get_alert_manager():
    """Get the global alert manager instance."""
    return alert_manager

# Convenience functions for easy integration
def check_website_alert(website_id, response_time, status_code):
    """Convenience function for website alerts."""
    return alert_manager.check_website_alert(website_id, response_time, status_code)

def check_synthetic_alert(check_id, recent_runs):
    """Convenience function for synthetic alerts."""
    return alert_manager.check_synthetic_alert(check_id, recent_runs)

def check_error_rate_alert(entity_id, error_rate):
    """Convenience function for error rate alerts."""
    return alert_manager.check_error_rate_alert(entity_id, error_rate)

if __name__ == "__main__":
    # Example usage
    alert_manager = get_alert_manager()

    # Test website alert
    check_website_alert("web-123", 6000, 200)

    # Test synthetic alert
    recent_runs = [
        {"timestamp": int(time.time() * 1000), "status": "failure"},
        {"timestamp": int(time.time() * 1000), "status": "failure"},
        {"timestamp": int(time.time() * 1000), "status": "failure"}
    ]
    check_synthetic_alert("chk-456", recent_runs)

    # Save history
    alert_manager.save_alert_history()
