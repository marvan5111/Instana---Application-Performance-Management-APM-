import logging
import logging.handlers
import os
from datetime import datetime

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

# Example usage and test
if __name__ == "__main__":
    log = get_logger("monitoring")
    log.info("Website check passed for https://example.com")
    log.warning("Slow response detected for https://api.example.com")
    log.error("Timeout occurred for https://example.com")
    log.debug("Debug information: response time 250ms")
