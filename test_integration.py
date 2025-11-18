import json
from monitor_runner import run_monitoring_checks
from monitor_validator import validate_monitoring_config
from synthetic_runner import run_synthetic_check
from logger import get_logger

log = get_logger("test_integration")

def test_monitoring_integration():
    """Test monitoring runner with generated configs"""
    log.info("Testing monitoring integration with generated configs")

    with open('data/instana/website_config.jsonl') as f:
        for line in f:
            config = json.loads(line)
            log.info(f"Validating config for {config['url']}")
            is_valid = validate_monitoring_config(config)
            if is_valid:
                log.info(f"Running check for {config['url']}")
                run_monitoring_checks(config)
            else:
                log.error(f"Invalid config for {config['url']}, skipping check")
            break  # Test only first config to avoid too many requests

def test_synthetic_integration():
    """Test synthetic runner with generated checks"""
    log.info("Testing synthetic integration with generated checks")

    with open('data/instana/synthetic_checks.jsonl') as f:
        for line in f:
            check = json.loads(line)
            log.info(f"Running synthetic check for {check['url']}")
            run_synthetic_check(check)
            break  # Test only first check

if __name__ == "__main__":
    test_monitoring_integration()
    test_synthetic_integration()
