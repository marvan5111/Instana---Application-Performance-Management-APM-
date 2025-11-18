import json
from monitor_runner import run_monitoring_checks
from monitor_validator import validate_monitoring_config
from synthetic_runner import run_synthetic_check
from logger import get_logger

log = get_logger("test_edge_cases")

def test_invalid_configs():
    """Test validation with invalid configs"""
    log.info("Testing invalid config validation")

    invalid_configs = [
        {"url": "not-a-url", "check_interval_seconds": 60, "timeout_ms": 5000, "expected_status_codes": [200], "alert_on_failure": True},
        {"url": "https://example.com", "check_interval_seconds": -1, "timeout_ms": 5000, "expected_status_codes": [200], "alert_on_failure": True},
        {"url": "https://example.com", "check_interval_seconds": 60, "timeout_ms": "not-a-number", "expected_status_codes": [200], "alert_on_failure": True},
        {"url": "https://example.com", "check_interval_seconds": 60, "timeout_ms": 5000, "expected_status_codes": [999], "alert_on_failure": True},
        {"url": "https://example.com", "check_interval_seconds": 60, "timeout_ms": 5000, "expected_status_codes": [200], "alert_on_failure": "not-a-bool"}
    ]

    for i, config in enumerate(invalid_configs):
        log.info(f"Testing invalid config {i+1}")
        is_valid = validate_monitoring_config(config)
        assert not is_valid, f"Config {i+1} should be invalid but passed validation"

def test_timeout_scenarios():
    """Test timeout handling"""
    log.info("Testing timeout scenarios")

    # Test with very short timeout
    timeout_config = {
        "url": "https://httpbin.org/delay/5",  # 5 second delay
        "timeout_ms": 1000,  # 1 second timeout
        "expected_status_codes": [200],
        "alert_on_failure": True
    }

    log.info("Testing timeout scenario")
    run_monitoring_checks(timeout_config)

def test_malformed_responses():
    """Test handling of malformed responses"""
    log.info("Testing malformed response handling")

    # Test with invalid status code expectation
    malformed_config = {
        "url": "https://httpbin.org/status/500",
        "timeout_ms": 5000,
        "expected_status_codes": [200],
        "alert_on_failure": True
    }

    log.info("Testing malformed response scenario")
    run_monitoring_checks(malformed_config)

if __name__ == "__main__":
    try:
        test_invalid_configs()
        log.info("Invalid config tests passed")
    except AssertionError as e:
        log.error(f"Invalid config test failed: {e}")

    test_timeout_scenarios()
    test_malformed_responses()

    log.info("Edge case testing completed")
