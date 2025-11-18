import requests
import time
from logger import get_logger

log = get_logger("synthetic_runner")

def run_synthetic_check(check_config):
    """
    Run a synthetic check based on the provided config.

    Args:
        check_config: Dict containing synthetic check configuration
    """
    url = check_config.get('url')
    method = check_config.get('method', 'GET')
    headers = check_config.get('headers', {})
    body = check_config.get('body')
    timeout = check_config.get('timeout_ms', 10000) / 1000  # Convert to seconds
    expected_status = check_config.get('expected_status', 200)

    try:
        start_time = time.time()
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=timeout)
        else:
            log.error(f"Unsupported HTTP method: {method}")
            return

        duration = int((time.time() - start_time) * 1000)  # ms

        if response.status_code == expected_status:
            log.info(f"Synthetic check passed for {url} - Status: {response.status_code}, Duration: {duration}ms")
        else:
            log.warning(f"Synthetic check failed for {url} - Expected {expected_status}, got {response.status_code}, Duration: {duration}ms")

    except requests.exceptions.Timeout:
        log.error(f"Synthetic check timeout for {url} after {timeout}s")
    except requests.exceptions.RequestException as e:
        log.error(f"Synthetic check request failed for {url}: {str(e)}")

# Example usage
if __name__ == "__main__":
    sample_check = {
        "url": "https://httpbin.org/get",
        "method": "GET",
        "headers": {"User-Agent": "SyntheticCheck/1.0"},
        "expected_status": 200,
        "timeout_ms": 5000
    }
    run_synthetic_check(sample_check)

    # Test POST
    sample_post_check = {
        "url": "https://httpbin.org/post",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": '{"test": "data"}',
        "expected_status": 200,
        "timeout_ms": 5000
    }
    run_synthetic_check(sample_post_check)
