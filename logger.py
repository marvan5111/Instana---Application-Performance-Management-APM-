import logging
import logging.handlers
import os
from datetime import datetime
from alerting import get_alert_manager

def get_logger(name: str, log_file: str = "monitoring.log", max_bytes: int = 1024*1024, backup_count: int = 5) -> logging.Logger:
    """
    Get a configured logger with console and rotating file output.

    Args:
        name: Logger name
        log_file: Log file path
        max_bytes: Maximum log file size before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # Already configured

    logger.setLevel(logging.DEBUG)

    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Formatter
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

class AlertingLogger:
    """Logger wrapper that can trigger alerts based on log levels and patterns."""

    def __init__(self, name: str, alert_on_errors: bool = True, alert_on_warnings: bool = False):
        self.logger = get_logger(name)
        self.alert_manager = get_alert_manager()
        self.alert_on_errors = alert_on_errors
        self.alert_on_warnings = alert_on_warnings
        self.failure_counts = {}  # Track consecutive failures for alerting

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, **kwargs)
        if self.alert_on_warnings:
            self._trigger_alert("warning", message)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, **kwargs)
        if self.alert_on_errors:
            self._trigger_alert("error", message)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, **kwargs)
        self._trigger_alert("critical", message)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, **kwargs)

    def _trigger_alert(self, level, message):
        """Trigger an alert for significant log events."""
        alert = {
            "type": "log",
            "level": level,
            "message": message,
            "timestamp": int(datetime.now().timestamp() * 1000),
            "severity": "high" if level in ["error", "critical"] else "medium"
        }
        self.alert_manager.trigger_alert(alert)

    def log_monitoring_result(self, check_type, target, success, response_time=None, error_msg=None):
        """Log monitoring results with potential alerting."""
        if success:
            self.info(f"{check_type} check passed for {target}" +
                     (f" - {response_time}ms" if response_time else ""))
            # Reset failure count on success
            self.failure_counts[target] = 0
        else:
            failure_count = self.failure_counts.get(target, 0) + 1
            self.failure_counts[target] = failure_count

            error_detail = f" - {error_msg}" if error_msg else ""
            self.error(f"{check_type} check failed for {target} (failure #{failure_count}){error_detail}")

            # Trigger alert after consecutive failures
            if failure_count >= 3:
                alert = {
                    "type": check_type,
                    "target": target,
                    "message": f"{check_type} check for {target} failed {failure_count} consecutive times",
                    "timestamp": int(datetime.now().timestamp() * 1000),
                    "severity": "high"
                }
                self.alert_manager.trigger_alert(alert)

# Example usage and test
if __name__ == "__main__":
    log = get_logger("monitoring")
    log.info("Website check passed for https://example.com")
    log.warning("Slow response detected for https://api.example.com")
    log.error("Timeout occurred for https://example.com")
    log.debug("Debug information: response time 250ms")

    # Test alerting logger
    alert_log = AlertingLogger("alert_test")
    alert_log.log_monitoring_result("website", "https://example.com", True, 250)
    alert_log.log_monitoring_result("website", "https://failing.com", False, error_msg="Connection timeout")
    alert_log.log_monitoring_result("website", "https://failing.com", False, error_msg="Connection timeout")
    alert_log.log_monitoring_result("website", "https://failing.com", False, error_msg="Connection timeout")
