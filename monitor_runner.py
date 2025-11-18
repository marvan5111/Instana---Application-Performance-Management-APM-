import requests
import time
from logger import get_logger

log = get_logger("monitor_runner")

def run_monitoring_checks(config):
    """
    Run monitoring checks based on the provided config.

    Args:
        config: Dict containing monitoring configuration
    """
    url = config.get('url')
    timeout = config.get('timeout_ms', 5000) / 1000  # Convert to seconds
    expected_codes = config.get('expected_status_codes', [200])

    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = int((time.time() - start_time) * 1000)  # ms

        if response.status_code in expected_codes:
            log.info(f"Website check passed for {url} - Status: {response.status_code}, Response time: {response_time}ms")
        else:
            log.warning(f"Website check failed for {url} - Expected {expected_codes}, got {response.status_code}, Response time: {response_time}ms")

    except requests.exceptions.Timeout:
        log.error(f"Timeout occurred for {url} after {timeout}s")
    except requests.exceptions.RequestException as e:
        log.error(f"Request failed for {url}: {str(e)}")

# Example usage
if __name__ == "__main__":
    sample_config = {
        "url": "https://httpbin.org/status/200",
        "timeout_ms": 5000,
        "expected_status_codes": [200]
    }
    run_monitoring_checks(sample_config)

    # Test failure
    sample_config_fail = {
        "url": "https://httpbin.org/status/404",
        "timeout_ms": 5000,
        "expected_status_codes": [200]
    }
    run_monitoring_checks(sample_config_fail)
