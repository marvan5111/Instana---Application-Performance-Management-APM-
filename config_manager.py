import json
import os
from datetime import datetime

class ConfigManager:
    """Manager for monitoring and alerting configurations."""

    def __init__(self, config_dir="configs"):
        self.config_dir = config_dir
        self.ensure_config_dir()

    def ensure_config_dir(self):
        """Ensure configuration directory exists."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)

    def save_website_config(self, configs):
        """Save website monitoring configurations."""
        path = os.path.join(self.config_dir, "website_config.json")
        with open(path, 'w') as f:
            json.dump(configs, f, indent=2)
        return path

    def load_website_config(self):
        """Load website monitoring configurations."""
        path = os.path.join(self.config_dir, "website_config.json")
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_synthetic_config(self, configs):
        """Save synthetic check configurations."""
        path = os.path.join(self.config_dir, "synthetic_config.json")
        with open(path, 'w') as f:
            json.dump(configs, f, indent=2)
        return path

    def load_synthetic_config(self):
        """Load synthetic check configurations."""
        path = os.path.join(self.config_dir, "synthetic_config.json")
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_alert_config(self, config):
        """Save alerting configuration."""
        path = os.path.join(self.config_dir, "alert_config.json")
        with open(path, 'w') as f:
            json.dump(config, f, indent=2)
        return path

    def load_alert_config(self):
        """Load alerting configuration."""
        path = os.path.join(self.config_dir, "alert_config.json")
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default config
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

    def create_default_website_config(self):
        """Create a default website monitoring configuration."""
        return [
            {
                "website_id": "homepage",
                "url": "https://example.com",
                "check_interval_seconds": 60,
                "timeout_ms": 5000,
                "expected_status_codes": [200, 201],
                "alert_on_failure": True,
                "tags": ["env:prod", "type:homepage"]
            },
            {
                "website_id": "api-health",
                "url": "https://api.example.com/health",
                "check_interval_seconds": 30,
                "timeout_ms": 3000,
                "expected_status_codes": [200],
                "alert_on_failure": True,
                "tags": ["env:prod", "type:api"]
            }
        ]

    def create_default_synthetic_config(self):
        """Create a default synthetic monitoring configuration."""
        return [
            {
                "check_id": "api-status",
                "name": "API Status Check",
                "type": "api",
                "url": "https://api.example.com/status",
                "method": "GET",
                "expected_status": 200,
                "timeout_ms": 5000,
                "frequency_seconds": 60,
                "locations": ["us-east", "eu-central"]
            },
            {
                "journey_id": "user-login-flow",
                "name": "User Login Journey",
                "type": "journey",
                "steps": [
                    {
                        "name": "Load Login Page",
                        "method": "GET",
                        "url": "https://example.com/login",
                        "expected_status": 200,
                        "timeout_ms": 5000,
                        "validations": [
                            {"type": "response_time", "max_ms": 2000},
                            {"type": "contains_text", "text": "login"}
                        ]
                    },
                    {
                        "name": "Submit Login",
                        "method": "POST",
                        "url": "https://example.com/login",
                        "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                        "body": "username=test&password=test",
                        "expected_status": 302,
                        "timeout_ms": 10000,
                        "validations": [
                            {"type": "response_time", "max_ms": 3000}
                        ]
                    },
                    {
                        "name": "Access Dashboard",
                        "method": "GET",
                        "url": "https://example.com/dashboard",
                        "expected_status": 200,
                        "timeout_ms": 5000,
                        "validations": [
                            {"type": "contains_text", "text": "welcome"}
                        ]
                    }
                ]
            }
        ]

    def validate_config(self, config_type, config):
        """Validate configuration structure."""
        if config_type == "website":
            required_fields = ["url", "timeout_ms", "expected_status_codes"]
            for field in required_fields:
                if field not in config:
                    raise ValueError(f"Missing required field: {field}")
        elif config_type == "synthetic":
            if "steps" in config:  # Multi-step journey
                if not config["steps"]:
                    raise ValueError("Journey must have at least one step")
                for step in config["steps"]:
                    if "method" not in step or "url" not in step:
                        raise ValueError("Each journey step must have method and url")
            else:  # Single check
                required_fields = ["url", "method", "expected_status"]
                for field in required_fields:
                    if field not in config:
                        raise ValueError(f"Missing required field: {field}")
        elif config_type == "alert":
            if "thresholds" not in config:
                raise ValueError("Alert config must have thresholds")

    def export_configs(self, output_dir="exported_configs"):
        """Export all configurations to a directory."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Export website configs
        website_configs = self.load_website_config()
        with open(os.path.join(output_dir, f"website_config_{timestamp}.json"), 'w') as f:
            json.dump(website_configs, f, indent=2)

        # Export synthetic configs
        synthetic_configs = self.load_synthetic_config()
        with open(os.path.join(output_dir, f"synthetic_config_{timestamp}.json"), 'w') as f:
            json.dump(synthetic_configs, f, indent=2)

        # Export alert configs
        alert_config = self.load_alert_config()
        with open(os.path.join(output_dir, f"alert_config_{timestamp}.json"), 'w') as f:
            json.dump(alert_config, f, indent=2)

        return output_dir

# Global config manager instance
config_manager = ConfigManager()

def get_config_manager():
    """Get the global config manager instance."""
    return config_manager

if __name__ == "__main__":
    # Example usage
    cm = get_config_manager()

    # Create and save default configs
    website_configs = cm.create_default_website_config()
    cm.save_website_config(website_configs)

    synthetic_configs = cm.create_default_synthetic_config()
    cm.save_synthetic_config(synthetic_configs)

    alert_config = cm.load_alert_config()
    cm.save_alert_config(alert_config)

    print("Default configurations created and saved.")

    # Export configs
    export_dir = cm.export_configs()
    print(f"Configurations exported to: {export_dir}")
