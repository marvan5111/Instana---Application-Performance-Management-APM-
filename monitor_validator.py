from logger import get_logger

log = get_logger("monitor_validator")

def validate_monitoring_config(config):
    """
    Validate monitoring configuration.

    Args:
        config: Dict containing monitoring configuration

    Returns:
        bool: True if valid, False otherwise
    """
    required_keys = ['url', 'check_interval_seconds', 'timeout_ms', 'expected_status_codes', 'alert_on_failure']
    errors = []

    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required key: {key}")

    if 'url' in config:
        url = config['url']
        if not isinstance(url, str) or not url.startswith(('http://', 'https://')):
            errors.append("URL must be a string starting with http:// or https://")

    if 'check_interval_seconds' in config:
        interval = config['check_interval_seconds']
        if not isinstance(interval, int) or interval <= 0:
            errors.append("check_interval_seconds must be a positive integer")

    if 'timeout_ms' in config:
        timeout = config['timeout_ms']
        if not isinstance(timeout, int) or timeout <= 0:
            errors.append("timeout_ms must be a positive integer")

    if 'expected_status_codes' in config:
        codes = config['expected_status_codes']
        if not isinstance(codes, list) or not all(isinstance(code, int) and 100 <= code <= 599 for code in codes):
            errors.append("expected_status_codes must be a list of valid HTTP status codes (100-599)")

    if 'alert_on_failure' in config:
        alert = config['alert_on_failure']
        if not isinstance(alert, bool):
            errors.append("alert_on_failure must be a boolean")

    if errors:
        for error in errors:
            log.error(f"Config validation error: {error}")
        return False
    else:
        log.info("Monitoring config validation passed")
        return True

# Example usage
if __name__ == "__main__":
    valid_config = {
        "url": "https://example.com",
        "check_interval_seconds": 60,
        "timeout_ms": 5000,
        "expected_status_codes": [200, 201],
        "alert_on_failure": True
    }
    print("Valid config:", validate_monitoring_config(valid_config))

    invalid_config = {
        "url": "not-a-url",
        "check_interval_seconds": -1,
        "timeout_ms": "not-a-number",
        "expected_status_codes": [999],
        "alert_on_failure": "not-a-bool"
    }
    print("Invalid config:", validate_monitoring_config(invalid_config))
