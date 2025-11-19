import requests
import time
import argparse
from datetime import datetime, timedelta
from logger import AlertingLogger
from alerting import check_synthetic_alert

alert_log = AlertingLogger("synthetic_runner")

# Store recent runs for alerting (in production, use a proper cache/database)
recent_runs_cache = {}

def run_synthetic_check(check_config, enable_alerts=True):
    """
    Run a synthetic check based on the provided config.

    Args:
        check_config: Dict containing synthetic check configuration
        enable_alerts: Whether to enable alerting for failures
    """
    url = check_config.get('url')
    method = check_config.get('method', 'GET')
    headers = check_config.get('headers', {})
    body = check_config.get('body')
    timeout = check_config.get('timeout_ms', 10000) / 1000  # Convert to seconds
    expected_status = check_config.get('expected_status', 200)
    check_id = check_config.get('check_id', url)

    try:
        start_time = time.time()
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=timeout)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, data=body, timeout=timeout)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, data=body, timeout=timeout)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, timeout=timeout)
        else:
            alert_log.error(f"Unsupported HTTP method: {method}")
            return

        duration = int((time.time() - start_time) * 1000)  # ms

        # Record the run for alerting
        run_record = {
            "timestamp": int(time.time() * 1000),
            "status": "success" if response.status_code == expected_status else "failure",
            "duration_ms": duration,
            "status_code": response.status_code
        }

        # Store recent runs (keep last 10 for alerting logic)
        if check_id not in recent_runs_cache:
            recent_runs_cache[check_id] = []
        recent_runs_cache[check_id].append(run_record)
        recent_runs_cache[check_id] = recent_runs_cache[check_id][-10:]  # Keep only last 10

        if response.status_code == expected_status:
            alert_log.log_monitoring_result("synthetic", url, True, duration)
        else:
            alert_log.log_monitoring_result("synthetic", url, False, duration,
                                          f"Expected {expected_status}, got {response.status_code}")

            # Check for alert condition
            if enable_alerts:
                check_synthetic_alert(check_id, recent_runs_cache[check_id])

    except requests.exceptions.Timeout:
        run_record = {
            "timestamp": int(time.time() * 1000),
            "status": "failure",
            "duration_ms": int(timeout * 1000),
            "status_code": 0
        }
        if check_id not in recent_runs_cache:
            recent_runs_cache[check_id] = []
        recent_runs_cache[check_id].append(run_record)
        recent_runs_cache[check_id] = recent_runs_cache[check_id][-10:]

        alert_log.log_monitoring_result("synthetic", url, False, error_msg=f"Timeout after {timeout}s")
        if enable_alerts:
            check_synthetic_alert(check_id, recent_runs_cache[check_id])
    except requests.exceptions.RequestException as e:
        run_record = {
            "timestamp": int(time.time() * 1000),
            "status": "failure",
            "duration_ms": 0,
            "status_code": 0
        }
        if check_id not in recent_runs_cache:
            recent_runs_cache[check_id] = []
        recent_runs_cache[check_id].append(run_record)
        recent_runs_cache[check_id] = recent_runs_cache[check_id][-10:]

        alert_log.log_monitoring_result("synthetic", url, False, error_msg=str(e))
        if enable_alerts:
            check_synthetic_alert(check_id, recent_runs_cache[check_id])

def run_multi_step_journey(journey_config, enable_alerts=True):
    """
    Run a multi-step user journey (login → search → checkout).

    Args:
        journey_config: Dict containing journey configuration with steps
        enable_alerts: Whether to enable alerting
    """
    journey_id = journey_config.get('journey_id', 'multi-step-journey')
    steps = journey_config.get('steps', [])

    alert_log.info(f"Starting multi-step journey: {journey_id}")

    journey_success = True
    total_duration = 0
    step_results = []

    for i, step in enumerate(steps):
        step_name = step.get('name', f'Step {i+1}')
        alert_log.info(f"Executing step {i+1}: {step_name}")

        try:
            start_time = time.time()

            # Execute the step
            if step['method'].upper() == 'GET':
                response = requests.get(step['url'], headers=step.get('headers', {}),
                                      timeout=step.get('timeout_ms', 10000)/1000)
            elif step['method'].upper() == 'POST':
                response = requests.post(step['url'], headers=step.get('headers', {}),
                                       data=step.get('body'), timeout=step.get('timeout_ms', 10000)/1000)
            else:
                raise ValueError(f"Unsupported method: {step['method']}")

            step_duration = int((time.time() - start_time) * 1000)
            total_duration += step_duration

            # Validate step
            expected_status = step.get('expected_status', 200)
            validations = step.get('validations', [])

            step_success = True
            if response.status_code != expected_status:
                step_success = False

            # Additional validations
            for validation in validations:
                if validation['type'] == 'response_time':
                    if step_duration > validation['max_ms']:
                        step_success = False
                elif validation['type'] == 'contains_text':
                    if validation['text'] not in response.text:
                        step_success = False

            step_results.append({
                'step': i+1,
                'name': step_name,
                'success': step_success,
                'duration_ms': step_duration,
                'status_code': response.status_code
            })

            if not step_success:
                journey_success = False
                alert_log.log_monitoring_result("journey_step", f"{journey_id}:{step_name}", False,
                                              step_duration, f"Step failed: {response.status_code}")
                break  # Stop journey on first failure
            else:
                alert_log.log_monitoring_result("journey_step", f"{journey_id}:{step_name}", True, step_duration)

        except Exception as e:
            journey_success = False
            step_results.append({
                'step': i+1,
                'name': step_name,
                'success': False,
                'duration_ms': 0,
                'error': str(e)
            })
            alert_log.log_monitoring_result("journey_step", f"{journey_id}:{step_name}", False, error_msg=str(e))
            break

    # Log overall journey result
    if journey_success:
        alert_log.log_monitoring_result("journey", journey_id, True, total_duration)
    else:
        alert_log.log_monitoring_result("journey", journey_id, False, total_duration,
                                      f"Journey failed at step {len(step_results)}")

    return {
        'journey_id': journey_id,
        'success': journey_success,
        'total_duration_ms': total_duration,
        'steps': step_results
    }

def run_synthetic_from_config(config_file, interval=300, alerts=True):
    """
    Run synthetic checks from a configuration file at regular intervals.

    Args:
        config_file: Path to JSON config file with synthetic check configs
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

    alert_log.info(f"Starting synthetic monitoring with {len(configs)} checks, interval {interval}s, alerts {'enabled' if alerts else 'disabled'}")

    while True:
        for config in configs:
            if 'steps' in config:
                # Multi-step journey
                run_multi_step_journey(config, enable_alerts=alerts)
            else:
                # Single check
                run_synthetic_check(config, enable_alerts=alerts)
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description='Instana Synthetic Monitoring Runner v1.3.0')
    parser.add_argument('--config', type=str, default='synthetic_checks.json',
                       help='Path to synthetic checks configuration file')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds')
    parser.add_argument('--alerts', action='store_true', default=True,
                       help='Enable alerting for failures')
    parser.add_argument('--no-alerts', action='store_true',
                       help='Disable alerting for failures')

    args = parser.parse_args()

    if args.no_alerts:
        args.alerts = False

    run_synthetic_from_config(args.config, args.interval, args.alerts)

# Example usage
if __name__ == "__main__":
    # Check if run as script with arguments
    import sys
    if len(sys.argv) > 1:
        main()
    else:
        # Legacy example usage
        sample_check = {
            "url": "https://httpbin.org/get",
            "method": "GET",
            "headers": {"User-Agent": "SyntheticCheck/1.0"},
            "expected_status": 200,
            "timeout_ms": 5000,
            "check_id": "sample-check"
        }
        run_synthetic_check(sample_check)

        # Test POST
        sample_post_check = {
            "url": "https://httpbin.org/post",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": '{"test": "data"}',
            "expected_status": 200,
            "timeout_ms": 5000,
            "check_id": "post-check"
        }
        run_synthetic_check(sample_post_check)

        # Example multi-step journey
        journey_config = {
            "journey_id": "ecommerce-flow",
            "steps": [
                {
                    "name": "Login",
                    "method": "POST",
                    "url": "https://httpbin.org/post",
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"username": "test", "password": "test"}',
                    "expected_status": 200,
                    "timeout_ms": 5000,
                    "validations": [
                        {"type": "response_time", "max_ms": 2000},
                        {"type": "contains_text", "text": "success"}
                    ]
                },
                {
                    "name": "Search",
                    "method": "GET",
                    "url": "https://httpbin.org/get?query=test",
                    "expected_status": 200,
                    "timeout_ms": 3000
                }
            ]
        }
        run_multi_step_journey(journey_config)
