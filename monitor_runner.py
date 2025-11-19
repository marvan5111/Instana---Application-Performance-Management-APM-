import requests
import time
import argparse
from logger import AlertingLogger
from alerting import check_website_alert

alert_log = AlertingLogger("monitor_runner")

def run_monitoring_checks(config, enable_alerts=True):
    """
    Run monitoring checks based on the provided config.

    Args:
        config: Dict containing monitoring configuration
        enable_alerts: Whether to enable alerting for failures
    """
    url = config.get('url')
    timeout = config.get('timeout_ms', 5000) / 1000  # Convert to seconds
    expected_codes = config.get('expected_status_codes', [200])
    website_id = config.get('website_id', url)

    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = int((time.time() - start_time) * 1000)  # ms

        if response.status_code in expected_codes:
            alert_log.log_monitoring_result("website", url, True, response_time)
        else:
            alert_log.log_monitoring_result("website", url, False, response_time,
                                          f"Expected {expected_codes}, got {response.status_code}")

            # Trigger alert if enabled
            if enable_alerts:
                check_website_alert(website_id, response_time, response.status_code)

    except requests.exceptions.Timeout:
        alert_log.log_monitoring_result("website", url, False, error_msg=f"Timeout after {timeout}s")
        if enable_alerts:
            check_website_alert(website_id, timeout * 1000, 0)  # Use timeout as response time
    except requests.exceptions.RequestException as e:
        alert_log.log_monitoring_result("website", url, False, error_msg=str(e))
        if enable_alerts:
            check_website_alert(website_id, 0, 0)  # No response time or status

def run_monitoring_from_config(config_file, interval=60, alerts=True):
    """
    Run monitoring checks from a configuration file at regular intervals.

    Args:
        config_file: Path to JSON config file with monitoring configs
        interval: Check interval in seconds
        alerts: Whether to enable alerts
    """
    import json

    try:
        with open(config_file, 'r') as f:
            configs = json.load(f)
    except FileNotFoundError:
        alert_log.error(f"Config file {config_file} not found")
        return

    alert_log.info(f"Starting monitoring with {len(configs)} checks, interval {interval}s, alerts {'enabled' if alerts else 'disabled'}")

    while True:
        for config in configs:
            run_monitoring_checks(config, enable_alerts=alerts)
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description='Instana Website Monitoring Runner v1.3.0')
    parser.add_argument('--config', type=str, default='website_config.json',
                       help='Path to monitoring configuration file')
    parser.add_argument('--interval', type=int, default=60,
                       help='Check interval in seconds')
    parser.add_argument('--alerts', action='store_true', default=True,
                       help='Enable alerting for failures')
    parser.add_argument('--no-alerts', action='store_true',
                       help='Disable alerting for failures')

    args = parser.parse_args()

    if args.no_alerts:
        args.alerts = False

    run_monitoring_from_config(args.config, args.interval, args.alerts)

# Example usage
if __name__ == "__main__":
    # Check if run as script with arguments
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Legacy example usage
        sample_config = {
            "url": "https://httpbin.org/status/200",
            "timeout_ms": 5000,
            "expected_status_codes": [200],
            "website_id": "sample-site"
        }
        run_monitoring_checks(sample_config)

        # Test failure
        sample_config_fail = {
            "url": "https://httpbin.org/status/404",
            "timeout_ms": 5000,
            "expected_status_codes": [200],
            "website_id": "failing-site"
        }
        run_monitoring_checks(sample_config_fail)
